@login_required
def delete_my_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        if request.method == "POST":
            comment.delete()
            return redirect("add_comment_to_post", comment.id)
        else:
            return render('comments/delete.html',{'comment': comment, "next": next})
    else:
        raise Http404