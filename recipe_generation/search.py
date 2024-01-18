from sentence_transformers import util

from embeddings import Embeddings


class Search:
    def __init__(self, embeddings: Embeddings):
        self.embeddings = embeddings

    def search_in_products(self, query_product_name):
        if index := self._search_in_embeddings(query_product_name, self.embeddings.product_embeddings):
            return [self.embeddings.product_names[index], self.embeddings.product_ids[index]]
        return None

    def search_in_removal_list(self, query_product_name):
        if self._search_in_embeddings(query_product_name, self.embeddings.removal_list_embeddings) is None:
            return False
        return True

    def search_in_ingredients_at_home(self, query_product_name):
        if self._search_in_embeddings(query_product_name, self.embeddings.ingredients_at_home_embeddings) is None:
            return False
        return True

    def search_in_recipe_db(self, query_product_name):
        if index := self._search_in_embeddings(query_product_name, self.embeddings.recipe_embeddings):
            return self.embeddings.recipes[index]
        return None

    def _search_in_embeddings(self, query, embeddings, threshold=0.7):
        query_embedding = self.embeddings.encode(query.lower())
        cos_sim = util.cos_sim(embeddings, query_embedding)
        results = []
        for i in range(len(cos_sim)):
            results.append(cos_sim[i][0])
        max_similarity_score = max(results)
        if max_similarity_score.item() < threshold:
            return None
        return results.index(max_similarity_score)
