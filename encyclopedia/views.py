from django.shortcuts import render
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error404.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": entry,
            "entry": markdown2.markdown(util.get_entry(entry))
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