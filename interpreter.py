import sys
import json
import os
import re

variables = {}
functions = {}
function_signatures = {}

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakLoop(Exception): pass
class ContinueLoop(Exception): pass

def evaluate_expression(expr, local_vars=None):
    scope = (local_vars or variables).copy()
    def try_cast(val):
        try: return int(val)
        except:
            try: return float(val)
            except: return val
    for k,v in scope.items():
        scope[k] = try_cast(v)
    def replace_call(m):
        parts = m.group(1).split()
        fn, *args = parts
        res = call_function(fn, [evaluate_expression(a, local_vars) for a in args])
        return str(res)
    expr = re.sub(r'call\s+([a-zA-Z_]\w*(?:\s+[^\s]+)*)', replace_call, expr)
    try: return eval(expr, {}, scope)
    except: return expr

def parse_type(s):
    return {"int":int,"float":float,"str":str,"bool":bool,"void":type(None)}.get(s, object)

def check_types(fn, args, types):
    for i,(a,t) in enumerate(zip(args,types)):
        if not isinstance(a,t):
            print(f"Warning: arg{i} expected {t.__name__}, got {type(a).__name__}")

def process_block(lines, idx):
    block=[]
    while idx<len(lines) and lines[idx].startswith("  "):
        block.append(lines[idx].strip())
        idx+=1
    return block, idx

def skip_conditional(lines, idx, keys):
    while idx<len(lines):
        line = lines[idx]
        if any(line.strip().startswith(k) for k in keys): return idx
        if not line.startswith("  "): break
        idx+=1
    return idx

def process_if_block(lines, index, local_vars=None):
    executed=False
    while index<len(lines):
        line = lines[index].strip()
        if line.startswith("if ") or line.startswith("elif "):
            if not executed:
                cond = line.split(None,1)[1].rstrip(":").strip()
                if evaluate_expression(cond, local_vars):
                    blk, ni = process_block(lines, index+1)
                    for l in blk: process_line(l, blk, 0, local_vars)
                    executed=True
                    index=ni
                else:
                    index = skip_conditional(lines, index+1, ["elif","else"])
                    continue
            else:
                index = skip_conditional(lines, index+1, ["elif","else"])
                continue
        elif line.startswith("else"):
            if not executed:
                blk, ni = process_block(lines, index+1)
                for l in blk: process_line(l, blk, 0, local_vars)
                executed=True
                index=ni
            else:
                index = skip_conditional(lines, index+1, ["elif","else"])
                continue
        else:
            break
        index+=1
    return index-1

def process_line(line, lines, index, local_vars=None):
    if line.startswith("ask "):
        prompt=line.split('"')[1]; var=line.split("save as")[1].strip()
        val=input(prompt+" ")
        try: val=int(val)
        except:
            try: val=float(val)
            except: pass
        (local_vars or variables)[var]=val

    elif line.startswith("say "):
        expr=line[4:].strip()
        print(evaluate_expression(expr, local_vars))

    elif line.startswith("let "):
        name,expr=line[4:].split(" be ",1)
        variables[name.strip()]=evaluate_expression(expr.strip(), local_vars)

    elif line.startswith("if "):
        return process_if_block(lines, index, local_vars)

    elif line.startswith("define "):
        parts=line[len("define "):].split("->")
        header=parts[0].strip()
        rt=parse_type(parts[1].strip()) if len(parts)>1 else type(None)
        tok=header.split()
        fn=tok[0]; params=tok[1:]
        pnames=[]; ptypes=[]
        for p in params:
            if ":" in p:
                n,t=p.split(":")
                pnames.append(n); ptypes.append(parse_type(t))
            else:
                pnames.append(p); ptypes.append(object)
        blk,ni=process_block(lines,index+1)
        functions[fn]=blk; function_signatures[fn]=(pnames,ptypes,rt)
        return ni-1

    elif line.startswith("call "):
        parts=line.split()
        fn=parts[1]; args=[evaluate_expression(a,local_vars) for a in parts[2:]]
        result=call_function(fn,args)
        (local_vars or variables)["_"]=result

    elif line.startswith("return "):
        raise ReturnValue(evaluate_expression(line[7:].strip(), local_vars))

    elif line.startswith("repeat "):
        n=int(evaluate_expression(line.split()[1], local_vars))
        blk,ni=process_block(lines,index+1)
        try:
            for _ in range(n):
                for l in blk:
                    try: process_line(l, blk, 0, local_vars)
                    except ContinueLoop: break
        except BreakLoop: pass
        return ni-1

    elif line.startswith("while "):
        cond=line[6:].strip()
        blk,ni=process_block(lines,index+1)
        try:
            while evaluate_expression(cond, local_vars):
                for l in blk:
                    try: process_line(l, blk, 0, local_vars)
                    except ContinueLoop: break
        except BreakLoop: pass
        return ni-1

    elif line=="break": raise BreakLoop()
    elif line=="continue": raise ContinueLoop()

    elif line.startswith("savejson "):
        fn=line.split()[1].strip('"')
        with open(fn,"w") as f: json.dump(variables,f)
        print(f"Variables saved to {fn}")

    elif line.startswith("loadjson "):
        fn=line.split()[1].strip('"')
        with open(fn) as f: variables.update(json.load(f))
        print(f"Variables loaded from {fn}")

    elif line.startswith("import "):
        fn=line.split()[1].strip('"')
        if not fn.endswith(".eng"): fn+=".eng"
        if os.path.exists(fn): run_file(fn)
        else: print(f"Import failed: {fn}")

    return index

def call_function(name, args):
    blk=functions.get(name,[])
    if name in function_signatures:
        pnames,ptypes,rt=function_signatures[name]
        check_types(name,args,ptypes)
        local={pnames[i]:args[i] for i in range(len(args))}
        try:
            for l in blk: process_line(l,blk,0,local)
        except ReturnValue as rv:
            if rt is not type(None) and not isinstance(rv.value,rt):
                print(f"Warning: return of '{name}' should be {rt.__name__}")
            return rv.value
        if rt is not type(None):
            print(f"Warning: '{name}' should return {rt.__name__}")
    else:
        local={f"arg{i}":args[i] for i in range(len(args))}
        try:
            for l in blk: process_line(l,blk,0,local)
        except ReturnValue as rv:
            return rv.value
    return None

def run_file(fn):
    with open(fn) as f: lines=f.readlines()
    idx=0
    while idx<len(lines):
        line=lines[idx].rstrip("\n")
        if not line.strip() or line.strip().startswith("#"):
            idx+=1; continue
        new_idx=process_line(line.strip(),lines,idx)
        idx = new_idx+1 if new_idx!=idx else idx+1

def run_repl():
    print("ENG REPL (type 'exit')")
    buf=[]
    while True:
        try:
            prompt = "... " if buf else ">>> "
            line=input(prompt)
            if line=="exit": break
            if line.strip()=="":
                for i in range(len(buf)):
                    process_line(buf[i].strip(), buf, i)
                buf=[]
            else:
                buf.append(line)
        except KeyboardInterrupt:
            print("\nExiting."); break
        except Exception as e:
            print("Error:", e)
            buf=[]

def main():
    if len(sys.argv)>1: run_file(sys.argv[1])
    else: run_repl()

if __name__=="__main__":
    main()
