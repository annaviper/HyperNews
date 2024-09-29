from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
import json
from django.utils import timezone


def index(request):
	return redirect('news')


def load_news_json():
	try:
		with open(settings.NEWS_JSON_PATH, 'r') as file:
			return json.load(file)
	except FileNotFoundError:
		return HttpResponse("JSON file not found", status=404)


def sort_by_date(news):
	for article in news:
		article['created'] = article['created'].split(' ')[0]

	dates = {}
	for article in news:
		date = article['created']
		if date not in dates:
			dates[date] = []

	news_by_date_dict = dates.copy()
	for article in news:
		news_by_date_dict[article['created']].append(article)

	news_by_date = []
	for date, articles in news_by_date_dict.items():
		news_by_date.append((date, articles))
	news_by_date.sort(key=lambda x: x[0], reverse=True)
	return news_by_date


def news(request):
	news = load_news_json()
	query = request.GET.get('q', '')

	if query:
		news = [n for n in news if query.lower() in n['title'].lower()]

	return render(request, 'news.html', {'news': sort_by_date(news)})


def article(request, target: int):
	data = load_news_json()

	for article in data:
		if article["link"] == target:
			return render(request, 'article.html', {'article': article})


def create_article(request):
	if request.method == 'POST':
		news = load_news_json()

		# get title and text from form
		title = request.POST.get('title')
		print(title)
		text = request.POST.get('text')
		print(text)

		# generate unique link
		print(news)
		ids = sorted([n['link'] for n in news], reverse=True)
		print(ids)

		# create article entry, save
		new_article = {
			'created': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current DateTime
			'link': ids[0] + 1,
			'text': text,
			'title': title
		}
		news.append(new_article)
		with open(settings.NEWS_JSON_PATH, 'w') as f:
			json.dump(news, f, indent=4)

		return redirect('/news/')
	else:
		return render(request, 'news/create.html')
