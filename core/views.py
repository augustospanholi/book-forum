from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from core.models import Post, Reply, Rules
from core.forms import PostForm, ReplyForm, RulesForm


def home(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')

    posts = Post.objects.filter(published=True).annotate(reply_count=Count('replies'))

    query = request.GET.get('q', '')
    if query:
        posts = posts.filter(title__icontains=query)

    order = request.GET.get('order', 'newest')
    if order == 'replies':
        posts = posts.order_by('-pinned', '-reply_count', '-created_at')
    else:
        posts = posts.order_by('-pinned', '-created_at')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    rules_obj = Rules.objects.first()
    stats = {
        'threads': Post.objects.filter(published=True).count(),
        'replies': Reply.objects.count(),
        'members': User.objects.filter(is_active=True).count(),
    }
    return render(request, 'core/home.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'query': query,
        'order': order,
        'rules': rules_obj,
        'stats': stats,
    })


def post_detail(request, post_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')

    post = get_object_or_404(Post, pk=post_id, published=True)
    replies = post.replies.all()
    form = ReplyForm()

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.post = post
            reply.author = request.user
            reply.save()
            messages.success(request, 'Reply posted!')
            return redirect('post_detail', post_id=post.id)

    return render(request, 'core/post_detail.html', {
        'post': post,
        'replies': replies,
        'form': form,
    })


def post_create(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to create a post.')
        return redirect('login')

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', post_id=post.id)

    return render(request, 'core/post_create.html', {'form': form})


def post_edit(request, post_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to edit a post.')
        return redirect('login')

    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('post_detail', post_id=post.id)

    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)

    return render(request, 'core/post_edit.html', {'form': form, 'post': post})


def post_delete(request, post_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to delete a post.')
        return redirect('login')

    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('post_detail', post_id=post.id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')

    return render(request, 'core/post_delete.html', {'post': post})


def profile(request, username):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')

    profile_user = get_object_or_404(User, username=username)
    all_posts = Post.objects.filter(author=profile_user, published=True)
    user_replies = Reply.objects.filter(author=profile_user)

    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/profile.html', {
        'profile_user': profile_user,
        'user_posts': page_obj,
        'total_posts': all_posts.count(),
        'reply_count': user_replies.count(),
        'page_obj': page_obj,
    })


def reply_edit(request, reply_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to edit a reply.')
        return redirect('login')

    reply = get_object_or_404(Reply, pk=reply_id)

    if request.user != reply.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this reply.')
        return redirect('post_detail', post_id=reply.post.id)

    form = ReplyForm(instance=reply)

    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reply updated successfully!')
            return redirect('post_detail', post_id=reply.post.id)

    return render(request, 'core/reply_edit.html', {'form': form, 'reply': reply})


def reply_delete(request, reply_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to delete a reply.')
        return redirect('login')

    reply = get_object_or_404(Reply, pk=reply_id)

    if request.user != reply.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this reply.')
        return redirect('post_detail', post_id=reply.post.id)

    post_id = reply.post.id
    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully!')
        return redirect('post_detail', post_id=post_id)

    return render(request, 'core/reply_delete.html', {'reply': reply})


def rules(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')

    rules_obj = Rules.objects.first()
    return render(request, 'core/rules.html', {'rules': rules_obj})


def rules_edit(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to access this page.')
        return redirect('login')

    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit the rules.')
        return redirect('rules')

    rules_obj = Rules.objects.first()
    form = RulesForm(instance=rules_obj)

    if request.method == 'POST':
        form = RulesForm(request.POST, instance=rules_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rules updated successfully!')
            return redirect('rules')

    return render(request, 'core/rules_edit.html', {'form': form})


def ban_user(request, username):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'You do not have permission to do this.')
        return redirect('home')

    target = get_object_or_404(User, username=username)

    if target == request.user:
        messages.error(request, 'You cannot ban yourself.')
        return redirect('profile', username=username)

    if target.is_staff:
        messages.error(request, 'You cannot ban another admin.')
        return redirect('profile', username=username)

    if request.method == 'POST':
        target.is_active = not target.is_active
        target.save()
        action = 'banned' if not target.is_active else 'unbanned'
        messages.success(request, f'User {target.username} has been {action}.')
        return redirect('profile', username=username)

    return redirect('profile', username=username)


def pin_post(request, post_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, 'You do not have permission to do this.')
        return redirect('post_detail', post_id=post_id)

    post = get_object_or_404(Post, pk=post_id, published=True)

    if request.method == 'POST':
        post.pinned = not post.pinned
        post.save()
        action = 'pinned' if post.pinned else 'unpinned'
        messages.success(request, f'Thread {action}.')

    return redirect('post_detail', post_id=post_id)


def resolve_post(request, post_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to do this.')
        return redirect('login')

    post = get_object_or_404(Post, pk=post_id, published=True)

    if request.user != post.author and not request.user.is_staff:
        messages.error(request, 'You do not have permission to do this.')
        return redirect('post_detail', post_id=post_id)

    if request.method == 'POST':
        post.resolved = not post.resolved
        post.save()
        action = 'marked as resolved' if post.resolved else 'reopened'
        messages.success(request, f'Thread {action}.')

    return redirect('post_detail', post_id=post_id)


def our_history(request):
    return render(request, 'core/our_history.html')


def contact(request):
    return render(request, 'core/contact.html')


def custom_404(request, exception):
    return render(request, '404.html', status=404)
