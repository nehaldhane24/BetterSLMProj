def customerCommentSummary(listOfComments):

    # import requests
    # url = f"https://mimir-prod.cisco.com/api/mimir/sora/customer_accountcomments_by_bug?bugId={bugId}"

    # payload={}
    # headers = {
    #     'Authorization': 'Bearer QJfFFgMT2fL0ylheu2SsMnvSFZqQ',
    # # 'Authorization': 'Bearer 4Y06smMYLwPzPtoaPkM5bUkcLmhj',
    # 'Cookie': 'mimir=eyJleHBpcmF0aW9uIjoiNDMyMDAiLCJleHBpcmVzIjoxNjYzODc0OTQ5LCJ1c2VyaWQiOiJpc2hhdWthdCJ9--46cc1a1db2e314eee604a4559b72d0b61c4c80af'
    # }

    # response = requests.request("GET", url, headers=headers, data=payload)
    
    # customer_comments=response.json()

    corpus_pre = listOfComments
    noOfComments=len(corpus_pre)
    #print(customer_comments)
    # for elem in customer_comments["data"]:
    #     comment=elem['accountSpecificComments']
    #     if comment is not None:
    #         corpus_pre.append(comment)
    #         print(comment)        
    #         noOfComments+=1
    

    print(noOfComments)
    

    # Removing redundancy by checking if ith comment is present in jth comment
    corpus=[]
    for i in range(0, noOfComments):
        add=True
        for j in range(0, noOfComments):
            if i==j:
                continue
            if corpus_pre[i] in corpus_pre[j]:
                add=False
        if add:
            corpus.append(corpus_pre[i])

    noOfComments=len(corpus)
    print(noOfComments)

    from sklearn.feature_extraction.text import TfidfVectorizer
    import numpy as np

    # Removing redundancy by matching similarity

    vect = TfidfVectorizer(min_df=1, stop_words="english")                                                                                                                                                                                                   
    tfidf = vect.fit_transform(corpus)                                                                                                                                                                                                                       
    pairwise_similarity = tfidf * tfidf.T 
    similarity_matrix=pairwise_similarity.toarray()

    #print(similarity_matrix)
    np.fill_diagonal(similarity_matrix, np.nan)      

    counter=0

    isRedundant=set()
    while counter<noOfComments:
        if counter in isRedundant:
            counter+=1
            continue
        for idx,similarity in enumerate(similarity_matrix[counter]):
            if similarity>0.5:
                isRedundant.add(idx)
        counter+=1

    summary=""
    noOfComments=0
    for idx,comment in enumerate(corpus):
        if idx in isRedundant:
            continue
        noOfComments+=1
        summary+=comment+'\n'
    #print(corpus)
    return(corpus,noOfComments)
