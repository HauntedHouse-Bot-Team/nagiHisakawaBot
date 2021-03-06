import wikipedia


def wikipediaSearch(search_text):
	response_string = ""
	wikipedia.set_lang("ja")
	search_response = wikipedia.search(search_text)
	if not search_response:
		response_string = "その単語は登録されていません。"
		return response_string
	try:
		wiki_page = wikipedia.page(search_response[0])
	except Exception as e:
		response_string = "エラーが発生しました。\n{}\n{}".format(e.message, str(e))
		return response_string
	wiki_content = wiki_page.content
	response_string += ""+wiki_content[0:wiki_content.find("。")] + "らしいですよbyうぃき"
	return response_string
