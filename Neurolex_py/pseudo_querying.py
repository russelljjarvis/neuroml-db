from rdflib import Graph
import os
from collections import defaultdict
import itertools
import random
import string
import re

vars=[]

PATH="/home/neuromine/Neurolex_py/new_group/"

inside=False
region=""
neurotransmitter=""
#"+"?"+combinations[index][0][0]+" ?x ?"+combinations[index][0][1]+" . "
in_quotes = '"[A-Za-z0-9_ ]+"'

def get_filename(line):
    ##print "line", re.findall(in_quotes,line)
    return re.findall(in_quotes,line)[0]

def neurons_by_neurotransmitter(neurolex_id,hash_table):
    g=Graph()
    g.parse(open(PATH+neurolex_id))
    
    query="""
            prefix property: <http://neurolex.org/wiki/Property-3A>
            SELECT ?neuron
            WHERE {
                 ?neuron property:Neurotransmitter ?a.
                ?a ?x \""""+neurolex_id+"""\"^^<http://www.w3.org/2001/XMLSchema#string>.}"""
                    
    ###print query               
    x= g.query(query)
    results=[]
    for y in x.result:
        try:
            ##print y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","")
            if hash_table[y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","")] not in results:
             
                #results.append(y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","") )
                results.append(hash_table[y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","")] )
        except:
            pass
    return results

def neurons_by_region(neurolex_id,hash_table):
    g=Graph()
    g.parse(open(PATH+neurolex_id))
    ###print neurolex_id
    query="""
            prefix property: <http://neurolex.org/wiki/Property-3A>
            SELECT ?neuron
            WHERE {
                 ?neuron property:Located_in ?a.
                ?a ?x \""""+neurolex_id+"""\"^^<http://www.w3.org/2001/XMLSchema#string>.}"""
    ###print query               
    x= g.query(query)
    results=[]
    for y in x.result:
        ###print y[0]
        ##print y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","")
        try:
            if hash_table[y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","")] not in results:
                #results.append(y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a",""))
                results.append(hash_table[y[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a","")] )
        except:
            ##print "no",y[0]
            pass
    ###print "final",results
    return results
            
def new_expand_regions(neurolex_id,associated_regions,hash_table):
    ###print "region", region
    ###print "in ",dict_vars[region]
    ##print neurolex_id
    region_graph=Graph()
    region_graph.parse(open("/home/neuromine/Neurolex_py/TheAlmightyPartsOfFile"))
    region_graph.parse(open(PATH+neurolex_id))
    
    query= "prefix property:<http://neurolex.org/wiki/Property-3A>  SELECT ?xid WHERE { ?x property:Id ?xid. ?x property:Is_part_of ?region. ?region property:Id \""+neurolex_id+'"^^<http://www.w3.org/2001/XMLSchema#string>. }'
    ###print "query",query
    x=region_graph.query(query)
    for result in  x.result:
        
        ##print "regions",result[0],"not just that",neurolex_id
        if result[0] not in associated_regions:
            associated_regions.append(result[0])
            new_expand_regions(result[0],associated_regions,hash_table)
        
    ##print "associated",associated_regions      
    return associated_regions
        ###print "regions",r[0],r[1]
    '''h=Graph()
        h.parse(open("new_group/"+r[1]))
        expand_regions("az",resp,{"az":'?az property:Id "'+r[2]+'"^^<http://www.w3.org/2001/XMLSchema#string> .'},h)
        ##print r[0],"part of",region
        new_graph=Graph()
        ##print "r",r[2]
        new_graph.parse(open("new_group/"+r[2]))
        new_query= "prefix property:<http://neurolex.org/wiki/Property-3A>  SELECT ?x WHERE { ?x property:Located_in ?re. ?re property:Id \""+r[2]+'"^^<http://www.w3.org/2001/XMLSchema#string> . }'
        ##print  "new query",new_query
        x=new_graph.query(new_query)
        for r in x.result:
            resp["neurons in related regions"].append(r[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a",""))
        '''

def find_relationships(neurolex_ids,hash_table):
    #print neurolex_ids
    g = Graph()
    resp=defaultdict(list)
    result_list=[]
    dict_vars={}
    results=defaultdict(list)
    dict_sub_regions=defaultdict(list)
    for index in xrange(len(neurolex_ids)):
        list_of_regions=new_expand_regions(neurolex_ids[index],[],hash_table)
        if list_of_regions!=[]:
            
            dict_sub_regions[neurolex_ids[index]].append(neurolex_ids[index])
            dict_sub_regions[neurolex_ids[index]].extend(list_of_regions)
        
    ##print "regions",dict_sub_regions

    where=""
    start="""  
    prefix property: <http://neurolex.org/wiki/Property-3A> """
    
    for index in xrange(len(neurolex_ids)):   
                        
        g.parse(open(PATH+neurolex_ids[index]))
        
        vars.append(''.join(random.choice(string.ascii_letters) for x in range(2)))
        dict_vars[vars[index]]=" ?"+vars[index]+' property:Id "'+neurolex_ids[index]+'"^^<http://www.w3.org/2001/XMLSchema#string> .'
        where=where+" ?"+vars[index]+' property:Id "'+neurolex_ids[index]+'"^^<http://www.w3.org/2001/XMLSchema#string> .'
        

    if len(vars)==1:
        if len(dict_sub_regions[neurolex_ids[0]])>1:
            for region in dict_sub_regions[neurolex_ids[0]]:
                ##print "yes"
                results["neurons in the same region"].extend(neurons_by_region(region,hash_table))
        
        else:
            
            final_where=" WHERE { ?"+vars[0]+" ?x ?y . "+where+" }"
            select=" SELECT ?"+vars[0]+" ?x ?y"
            query=start+select+final_where+'FILTER(STRSTARTS(STR(?x), "http://neurolex.org/wiki/Special:URIResolver/Property-3A"))'
            resp1=g.query(query)
            tried=[]
            for resp in resp1.result:


		if "Neurotransmitter" in resp[1]:
                        if resp[2] not in tried:
                            tried.append(resp[2])
                            try:
                                results["neurons with the same neurotransmitter"].extend(neurons_by_neurotransmitter(hash_table[resp[2].lower().replace("http://neurolex.org/wiki/category-3a","").replace("_"," ").replace(" cell","").replace(" neuron","")],hash_table))
                            except:
                                pass


                if "Located_in" in resp[1]:
                	if resp[2] not in tried:
                      	    tried.append(resp[2])
                            #print"yes", resp[2]
                            list_of_regions=new_expand_regions(hash_table[resp[2].lower().replace("http://neurolex.org/wiki/category-3a","").replace("_"," ").replace(" cell","").replace(" neuron","")],[],hash_table)
                            list_of_regions.append(hash_table[resp[2].lower().replace("http://neurolex.org/wiki/category-3a","").replace("_"," ").replace(" cell","").replace(" neuron","")])
                            #print "regions",list_of_regions
                            for region in list_of_regions:
                                
                                results["neurons from the same region"].extend(neurons_by_region(region,hash_table))
                    
    
            ##print "rr",results
            final_where=" WHERE { ?y ?x ?"+vars[0]+" . "+where+" }"
            select=" SELECT ?y ?x ?"+vars[0]
            query=start+select+final_where+'FILTER(STRSTARTS(STR(?x), "http://neurolex.org/wiki/Special:URIResolver/Property-3A"))'

            resp2=g.query(query)
            tried=[]
            for resp in resp2.result:
                try:
                  
                        '''if "Located_in" in resp[1]:
                            if resp[2] not in tried:
                                tried.append(resp[2])
                                results["neurons from the same region"+resp[2]].append(neurons_by_region(neurolex_ids[index]))'''
                        
                        if "Neurotransmitter" in resp[1]:
                            if resp[2] not in tried:
                                tried.append(resp[2])
                                results["neurons with the same neurotransmitter"].extend(neurons_by_neurotransmitter(neurolex_ids[index],hash_table))
                                results["neurons with the same neurotransmitter"]=list(set(results["neurons with the same neurotransmitter"]))
                except:
                    pass
        
        ##print results
        return results
    
    
    elif len(vars)==2:
	#print "yes"
        pairs=itertools.permutations(vars,2)
        pairs=list(pairs)
    
        for pair in pairs:
            final_where=" WHERE { ?"+pair[0]+" ?x ?"+pair[1]+". "+where+" }"
            select=" SELECT ?"+pair[0]+" ?x ?"+pair[1]
            old_query=start+select+final_where+'FILTER(STRSTARTS(STR(?x), "http://neurolex.org/wiki/Special:URIResolver/Property-3A"))'
            for key,value in dict_sub_regions.items():

                for replacement in value:
                    
                    new_query=old_query.replace(key,replacement)
                    ##print "constructed",new_query
                    x=g.query(new_query)
                    if len(x.result)>0:
                        if x.result not in result_list:
                            result_list.append(x.result)
                            ###print result_list
                            #print "inter",x.result
                            ##print "inserting", x.result[0][1]
                            results["similar neurons"].extend(recommendation(g,new_query,vars,dict_vars,[x.result[0][1]],dict_sub_regions,hash_table))
                #recommendation(g,x.result[0][0],x.result[0][1],x.result[0][2])
        ##print results
	if len(results["similar neurons"])!=0:
        	return results
          
        final_where=" WHERE { ?z ?x ?"+pair[0]+". ?z ?y ?"+pair[1]+". "+where+" }"
        select=" SELECT ?"+pair[0]+" ?z ?"+pair[1]
        query=start+select+final_where+'FILTER(STRSTARTS(STR(?x), "http://neurolex.org/wiki/Special:URIResolver/Property-3A"))'

        print "constructedquery", query
        x=g.query(query)
        if len(x.result)>0:
            #print x.result
            recommendation(g,query,vars,dict_vars,[x.result[0][1]],dict_sub_regions,hash_table)
            #recommendation(g,x.result[0][0],x.result[0][1],x.result[0][2])
            ##print "return"
            #return 2, x.result'''
            
        final_where=" WHERE { ?"+pair[0]+" ?x ?z. ?"+pair[1]+" ?y ?z. "+where+" }"
        select=" SELECT ?"+pair[0]+" ?z ?"+pair[1]
        query=start+select+final_where
        ##print "constructedquery", query
        x=g.query(query)
        if len(x.result)>0:
            ##print x.result
            recommendation(g,query,vars,dict_vars,[x.result[0][1]],dict_sub_regions,hash_table)
            #recommendation(g,x.result[0][0],x.result[0][1],x.result[0][2])
            return 2, x.result

	
            
    
    pairs=itertools.permutations(vars,2)
    pairs=list(pairs)            
        
    if len(vars)==3:
        combinations=itertools.permutations(pairs,len(vars)-1)
        combinations=list(combinations)

        for index in xrange(len(combinations)):
            #+" . "+"?"+combinations[index][1][0]+" ?y ?"+combinations[index][1][1]+
            if ((combinations[index][0][0]== combinations[index][1][0] or combinations[index][0][0]== combinations[index][1][1]) and (combinations[index][0][1]== combinations[index][1][0] or combinations[index][0][1]== combinations[index][1][1]))==False:
                final_where=" WHERE { ?"+combinations[index][0][0]+" ?x ?"+combinations[index][0][1]+" . "+"?"+combinations[index][1][0]+" ?y ?"+combinations[index][1][1]+" . "+where+" }"
                select=" SELECT ?"+combinations[index][0][0]+" ?x ?"+combinations[index][0][1]+" ?"+combinations[index][1][0]+" ?y ?"+combinations[index][1][1]
                query=start+select+final_where            
                ###print query
                x=g.query(query)
            
                if len(x.result)>0:
                    recommendation(g,query,vars,dict_vars,[x.result[0][1],x.result[0][4]])
                    return 3, x.result

'''def expand_regions(region,resp,dict_vars,g):
    ###print "region", region
    ###print "in ",dict_vars[region]
    g.parse(open("TheAlmightyPartsOfFile"))
    query= "prefix property:<http://neurolex.org/wiki/Property-3A>  SELECT ?x ?id ?mid WHERE { ?x property:Id ?mid. ?x property:Is_part_of ?"+region+". ?"+region+" property:Id ?id. "+dict_vars[region]+" }"
    ##print "query",query
    x=g.query(query)
    for r in  x.result:
        ###print "regions",r[0],r[1]
        h=Graph()
        h.parse(open("new_group/"+r[1]))
        expand_regions("az",resp,{"az":'?az property:Id "'+r[2]+'"^^<http://www.w3.org/2001/XMLSchema#string> .'},h)
        ##print r[0],"part of",region
        new_graph=Graph()
        ##print "r",r[2]
        new_graph.parse(open("new_group/"+r[2]))
        new_query= "prefix property:<http://neurolex.org/wiki/Property-3A>  SELECT ?x WHERE { ?x property:Located_in ?re. ?re property:Id \""+r[2]+'"^^<http://www.w3.org/2001/XMLSchema#string> . }'
        ##print  "new query",new_query
        x=new_graph.query(new_query)
        for r in x.result:
            resp["neurons in related regions"].append(r[0].lower().replace("_"," ").replace(" neuron","").replace(" cell","").replace("http://neurolex.org/wiki/category-3a",""))
        
    return resp'''
                
def recommendation(g,query,vars,dict_vars,rel,dict_sub_regions,hash_table):
    resp=defaultdict(list)
    result_list=[]

    
    
    
    '''for r in rel:
        if str(r)=='http://neurolex.org/wiki/Special:URIResolver/Property-3ALocated_in':
            ##print new_rel
            index=new_rel.index('http://neurolex.org/wiki/Special:URIResolver/Property-3ALocated_in')
            ##print "rel",rel
            ##print "index",index
            isLocated=True
    '''
    
    for var in vars:
        #print rel
        for key,value in dict_sub_regions.items():
            for v in value:
                
                g.parse(PATH+v)
                new_query=query.replace(dict_vars[var],"")
                new_query=new_query.replace(key,v)
                new_query=new_query.replace(" ?x "," <"+rel[0]+"> ")
                new_query=new_query.replace(" <"+rel[0]+"> "," ",1)
                try:
                    new_query=new_query.replace(" ?y "," <"+rel[1]+"> ")
                    new_query=new_query.replace(" <"+rel[1]+"> "," ",1)
                except:
                    pass
                try:
                    new_query=new_query.replace(" ?z "," <"+rel[2]+"> ")
                    new_query=new_query.replace(" <"+rel[2]+"> "," ",1)
                except:
                    pass
        
        #query
        
                #print "new",new_query
                results= g.query(new_query).result
    
                for result in results:
                    ##print result
                    ###print "list",result_list
                    ###print "result---",re.findall(in_quotes,dict_vars[var])
                    ###print result
                    for val in result:
                        try:
                            if hash_table[val.replace("http://neurolex.org/wiki/Category-3A","").lower().replace("_"," ").replace(" neuron","").replace(" cell","")] not in result_list:
                                #print val.replace("http://neurolex.org/wiki/Category-3A","").lower().replace("_"," ").replace(" neuron","").replace(" cell","")
                                result_list.append(hash_table[val.replace("http://neurolex.org/wiki/Category-3A","").lower().replace("_"," ").replace(" neuron","").replace(" cell","")])
                                ##print hash_table[val.replace("http://neurolex.org/wiki/Category-3A","").lower().replace("_"," ").replace(" neuron","").replace(" cell","")]
                        except:
                            pass
    ##print result_list
    return list(set(result_list))
    ###print r2.result
    
    
