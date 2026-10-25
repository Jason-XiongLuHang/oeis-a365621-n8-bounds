"""Portable, stdlib-only certification of the A365621(8) evidence.

python -B verify_release.py --inputs inputs --output receipt.json --rebuild
Optional: --cuts dual_cuts_k14.json
The script never imports a producer or optimization library and writes only
the explicitly requested NEW receipt. It does not verify SAT UNSAT proofs.
"""
import argparse,collections,hashlib,itertools,json,platform,sys,time
from datetime import datetime,timezone
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def normalized(animal):
    x=min(z.real for z in animal);y=min(z.imag for z in animal)
    return frozenset(z-complex(x,y) for z in animal)
def variants(animal):
    values=set()
    for r in (1,1j,-1,-1j):
        for reflected in (False,True):
            q=normalized([r*(z.conjugate() if reflected else z) for z in animal])
            values.add(tuple(sorted((int(z.real),int(z.imag)) for z in q)))
    return sorted(values)
def connected(animal):
    rest=set(animal);todo=[rest.pop()]
    for z in todo:
        for p in (z+1,z-1,z+1j,z-1j):
            if p in rest:rest.remove(p);todo.append(p)
    return not rest
def overlap_move(source,targets):
    for target in targets:
        counts=collections.Counter((x-u,y-v) for x,y in source for u,v in target)
        if 7 in counts.values():return True
    return False
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--inputs',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--rebuild',action='store_true');p.add_argument('--cuts',type=Path)
    args=p.parse_args()
    if args.output.exists():raise FileExistsError('Refusing to overwrite existing receipt: '+str(args.output))
    start=time.perf_counter();stage='inputs'
    receipt=dict(status='IN_PROGRESS',utc_start=datetime.now(timezone.utc).isoformat(),python=sys.version,
        platform=platform.platform(),script_sha256=sha(Path(__file__)),rebuild_requested=args.rebuild,
        solver_imported=False,optimization_performed=False,UNSAT_proof_verified=False)
    try:
        names=('graph_n8.json','UPPER17.json','LOWER14_RATIONAL.json','independent_highs17.json')
        sources={name:args.inputs/name for name in names}
        receipt['input_sha256']={name:sha(path) for name,path in sources.items()}
        graph=load(sources['graph_n8.json']);upper=load(sources['UPPER17.json'])
        lower=load(sources['LOWER14_RATIONAL.json']);moves=load(sources['independent_highs17.json'])
        stage='shape syntax/connectivity/D4'
        raw=graph['vertices'];assert len(raw)==369
        assert all(len(p)==8 and all(len(c)==2 and all(type(t) is int for t in c) for c in p) for p in raw)
        points=[tuple(map(tuple,p)) for p in raw]
        animals=[frozenset(complex(x,y) for x,y in p) for p in points]
        assert all(len(a)==8 and connected(a) for a in animals)
        all_variants=[variants(a) for a in animals]
        assert len({v[0] for v in all_variants})==369
        assert all(p==v[0] for p,v in zip(points,all_variants))
        edges=[tuple(e) for e in graph['edges']]
        assert len(edges)==len(set(edges))==6544 and all(type(u) is type(v) is int and 0<=u<v<369 for u,v in edges)
        receipt.update(vertices=369,edges=6544,rook_connectivity=True,distinct_D4_orbits=True,canonical_representatives=True)
        semantic=dict(vertices=raw,edges=[list(e) for e in sorted(edges)])
        receipt['graph_semantic_sha256']=hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if args.rebuild:
            stage='fixed enumeration and all-pair geometric edges'
            fixed={frozenset({0j})};counts=[]
            for n in range(1,9):
                if n>1:
                    generated=set()
                    for a in fixed:
                        border={z+d for z in a for d in (1,-1,1j,-1j)}-a
                        for z in border:generated.add(normalized(a|{z}))
                    fixed=generated
                counts.append(len(fixed));assert len(fixed)==[1,2,6,19,63,216,760,2725][n-1]
            assert {variants(a)[0] for a in fixed}=={v[0] for v in all_variants}
            generated={(u,v) for u in range(369) for v in range(u+1,369) if overlap_move(points[u],all_variants[v])}
            assert generated==set(edges)
            receipt.update(fixed_counts=counts,complete_free_shape_set_rebuilt=True,all_67896_pairs_checked=True)
        else:receipt.update(complete_free_shape_set_rebuilt=False,all_67896_pairs_checked=False,
            completeness_scope='369 distinct connected canonical shapes checked; full enumeration/all-edge certification requires --rebuild')
        stage='upper and explicit moves';ids=upper['selected_ids'];chosen=set(ids)
        assert len(ids)==len(chosen)==17 and all(type(i) is int and 0<=i<369 for i in ids)
        assert upper['selected_shapes']==[raw[i] for i in ids]
        assert len(moves['coverage'])==len({r['target'] for r in moves['coverage']})==369
        assert sorted(moves['selected_vertex_ids'])==sorted(ids)
        for row in moves['coverage']:
            t=row['target'];u=row['selected'];assert type(t) is int and 0<=t<369 and u in chosen
            if row.get('self'):assert t==u;continue
            m=row['move'];a=set(points[u]);removed=set(map(tuple,m['remove']));added=set(map(tuple,m['add']))
            assert len(removed)==len(added)==1 and removed<=a and not added&a
            result=a-removed|added
            assert len(result)==8 and len(result&a)==7
            assert set(map(tuple,m['common_cells']))==result&a
            assert connected({complex(x,y) for x,y in result})
            assert variants({complex(x,y) for x,y in result})[0]==all_variants[t][0]
            dx,dy=m['translation'];assert type(dx) is type(dy) is int
            assert {(x+dx,y+dy) for x,y in all_variants[t][m['orientation_index']]}==result
        for t in range(369):
            assert t in chosen or any(overlap_move(points[u],all_variants[t]) for u in ids)
        receipt.update(upper=17,upper_coordinates_match=True,all_369_explicit_moves_checked=True,
            all_369_targets_independently_geometrically_covered=True)
        stage='integer dual';w=lower['weights'];D=lower['denominator']
        assert len(w)==369 and all(type(t) is int and t>=0 for t in w) and type(D) is int and D>0
        closed=[{i} for i in range(369)]
        for u,v in edges:closed[u].add(v);closed[v].add(u)
        loads=[sum(w[x] for x in a) for a in closed]
        assert max(loads)<=D and sum(w)==lower['sum_numerator'] and loads==lower['all_column_loads']
        assert (sum(w)+D-1)//D==14
        receipt.update(lower=14,all_369_integer_dual_constraints_checked=True,weight_sum=sum(w),D=D,max_column_weight=max(loads))
        # Raw graph hashes can differ because an independently rebuilt graph has
        # different metadata/serialization. All mathematics above is rederived.
        actual_graph_hash=receipt['input_sha256']['graph_n8.json']
        receipt['raw_graph_bindings']={
            'supplied_graph_sha256':actual_graph_hash,
            'lower_declared_graph_sha256':lower.get('graph_sha256'),
            'move_record_declared_graph_sha256':moves.get('graph_sha256'),
            'lower_declared_hash_matches':lower.get('graph_sha256')==actual_graph_hash,
            'moves_declared_hash_matches':moves.get('graph_sha256')==actual_graph_hash,
            'scope':'All coverage and dual inequalities rederived on supplied graph; no claim of byte equality for a mismatching producer hash.'}
        assert moves['witness_sha256']==receipt['input_sha256']['UPPER17.json']
        if args.cuts:
            stage='threshold-specific cuts';cuts=load(args.cuts);k=cuts['k'];slack=k*D-sum(w)
            assert type(k) is int and k>=1 and cuts['D']==D and cuts['W']==sum(w) and cuts['slack']==slack
            assert cuts['lower_certificate_sha256']==receipt['input_sha256']['LOWER14_RATIONAL.json']
            expected=[i for i in range(369) if D-loads[i]>slack]
            assert cuts['forbidden']==expected
            eligible=[i for i in range(369) if i not in set(expected)]
            expected_pairs=[[u,v] for u,v in itertools.combinations(eligible,2) if 2*D-sum(w[x] for x in closed[u]|closed[v])>slack]
            assert cuts['pairs']==expected_pairs
            receipt['cuts']=dict(status='VERIFIED',sha256=sha(args.cuts),k=k,singletons=len(expected),pairs=len(expected_pairs),slack=slack,
                declared_graph_sha256=cuts.get('graph_sha256'),input_graph_sha256=actual_graph_hash,
                graph_byte_hash_matches=cuts.get('graph_sha256')==actual_graph_hash,
                graph_binding='Every cut independently rederived on supplied graph; producer bytes not asserted equal when hashes differ.',
                threshold_specific=True,UNSAT_proof_verified=False)
        receipt.update(status='VERIFIED',exact_value='UNKNOWN',certified_interval=[14,17],
            total_seconds=time.perf_counter()-start,utc_end=datetime.now(timezone.utc).isoformat(),peak_memory='UNKNOWN (not measured)')
    except Exception as e:
        receipt.update(status='FAILED',phase=stage,error=repr(e),total_seconds=time.perf_counter()-start)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
        raise
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(receipt),flush=True)
if __name__=='__main__':main()
