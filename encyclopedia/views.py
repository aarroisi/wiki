from django.shortcuts import render
from . import util
import markdown2
from django.core.files import File
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error404.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "content": markdown2.markdown(util.get_entry(entry))
        })

def search(request):
    if request.method == "GET":
        txt = request.GET['q']
        titles = util.list_entries()
        entries = [i.lower() for i in util.list_entries()]
        if txt in entries:
            txt = titles[entries.index(txt)]
            return render(request, "encyclopedia/entry.html", {
                "title": txt,
                "entry": util.get_entry(txt)
                })
        else:
            close = []
            for i,j in zip(entries,titles):
                if txt in i:
                    close.append(j)
            entries = list(set(close))
            return render(request, "encyclopedia/search_result.html", {
                "entries": close
            })

def new_wiki(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_wiki.html")
    else:
        entries = [i.lower() for i in util.list_entries()]
        title = request.POST['title']
        content = request.POST['content']
        content = "# "+title+"\n\n"+content
        if title.lower() in entries:
            messages.error(request, 'Entry already exists.')
            return HttpResponseRedirect(reverse("new_wiki"))
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("new_wiki"))

def edit_entry(request, entry):
    if request.method == "GET":
        return render(request, "encyclopedia/edit_entry.html", {
            "entry": entry,
            "content": util.get_entry(entry)
        })
    else:
        if request.POST['save'] == "1":
            content = request.POST['content']
            util.save_entry(entry, content)
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': entry}))

def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': entry}))