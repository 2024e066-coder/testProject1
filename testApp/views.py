from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import Lecture, Review, Like
from .forms import ReviewForm, SignUpForm


# =====================
# 講義一覧・詳細
# =====================

def lecture_list(request):
    lectures = Lecture.objects.all()
    return render(request, "reviews/lecture_list.html", {
        "lectures": lectures
    })


def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    reviews = Review.objects.filter(lecture=lecture)

    return render(request, "reviews/lecture_detail.html", {
        "lecture": lecture,
        "reviews": reviews
    })


# =====================
# レビュー CRUD
# =====================

@login_required
def review_create(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.lecture = lecture
            review.user = request.user
            review.save()
            return redirect("lecture_detail", lecture_id=lecture.id)
    else:
        form = ReviewForm()

    return render(request, "reviews/review_form.html", {
        "form": form
    })


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("lecture_detail", lecture_id=review.lecture.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("lecture_detail", lecture_id=review.lecture.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/review_form.html", {
        "form": form,
        "edit": True
    })


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if review.user != request.user:
        return redirect("lecture_detail", lecture_id=review.lecture.id)

    if request.method == "POST":
        review.delete()
        return redirect("lecture_detail", lecture_id=review.lecture.id)

    return render(request, "reviews/review_confirm_delete.html", {
        "review": review
    })


# =====================
# 認証（新規登録）
# =====================

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("lecture_list")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {
        "form": form
    })


# =====================
# いいね機能
# =====================

@login_required
def lecture_like(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        lecture=lecture
    )

    if not created:
        like.delete()

    return redirect("lecture_detail", lecture_id=lecture.id)



@login_required
def review_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        review=review
    )

    if not created:
        like.delete()

    return redirect("lecture_detail", lecture_id=review.lecture.id)

def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    reviews = Review.objects.filter(lecture=lecture)

    liked_review_ids = []
    liked_lecture = False

    if request.user.is_authenticated:
        liked_review_ids = Like.objects.filter(
            user=request.user,
            review__in=reviews
        ).values_list("review_id", flat=True)

        liked_lecture = Like.objects.filter(
            user=request.user,
            lecture=lecture
        ).exists()

    return render(request, "reviews/lecture_detail.html", {
        "lecture": lecture,
        "reviews": reviews,
        "liked_review_ids": liked_review_ids,
        "liked_lecture": liked_lecture,
    })

from django.db.models import Avg

def lecture_list(request):
    lectures = Lecture.objects.all()

    # GETパラメータ取得
    keyword = request.GET.get("keyword")
    min_rating = request.GET.get("rating")
    order = request.GET.get("order")

    # 🔍 授業名検索
    if keyword:
        lectures = lectures.filter(title__icontains=keyword)

    # ⭐ 平均評価でフィルタ
    if min_rating:
        lectures = lectures.annotate(
            avg_rating=Avg("reviews__rating")
        ).filter(avg_rating__gte=min_rating)

    # ↕ 並び替え
    if order == "new":
        lectures = lectures.order_by("-id")
    elif order == "rating":
        lectures = lectures.annotate(
            avg_rating=Avg("reviews__rating")
        ).order_by("-avg_rating")

    return render(request, "reviews/lecture_list.html", {
        "lectures": lectures,
    })
