from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import products,Catogaries,Review
from django.db.models import Avg,Count,F

# see product details
def product_details(request,pk):
    product = products.objects.get(id=pk)
    reviews= product.review.all()
    # calcualte average rating
    status=Review.objects.filter(product=product).aggregate(
        average_rating=Avg('rating')
    )
    average_rating=status['average_rating']
    if average_rating is not None:
        average_rating=round(average_rating,1)
    else:
        average_rating=0.0
    #total reviews by rating
    star_counts={}
    for i in range(1,6):
        # count = review_count.filter(rating=i).count()
        count = Review.objects.filter(product=product,rating=i).count()
        star_counts[str(i)] = count
    total_reviews = Review.objects.filter(product=product).count()
    star_percentage={}

    for star , count in star_counts.items():
        percentage=(count / total_reviews * 100 ) if total_reviews >0 else 0
        star_percentage[star] = round(percentage)
    # reviews = Review.objects.filter(product=product)
    # print(product.review.total_count)
    context= {
        'product': product,
        'reviews': reviews,
        'average_rating':average_rating,
        'star_percentage':star_percentage
    }
    return render(request,'product_detaile.html',context)

#add review 
def add_review(request):
    if request.POST and ('product_review') in request.POST:
        try:
            print(request.POST)
            pk = request.POST.get('product')
            product = products.objects.get(id=pk)
            comment = request.POST.get('comment')
            comment_TITLE= request.POST.get('comment_title')
            rating = request.POST.get('rating')
            image1= request.FILES.get('image1')
            image2= request.FILES.get('image2')
            image3= request.FILES.get('image3')
            user=request.user.customer_profile
            reviews=Review.objects.create(
                product=product, 
                comment=comment, 
                comment_title=comment_TITLE,
                rating=rating,
                user=user
            )
            if request.FILES.get('image1'):
                reviews.image1=image1
            if request.FILES.get('image2'):
                reviews.image2=image2
            if request.FILES.get('image3'):
                reviews.image3=image3
            print(reviews)
            reviews.save()
            previous_page = request.META.get('HTTP_REFERER')
            return redirect(previous_page)
        except Exception as e:
            print(e)
    return redirect('show_page')

#product listing by catagoris
def product_list(request,catagoris):
    cat=Catogaries.objects.get(name=catagoris)
    product=cat.products.all()
    paginator = Paginator(product,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'product':page_obj
    }
    return render(request,'products.html',context)

#normal product listing
def product_list1(request):
    product=products.objects.all()
    paginator = Paginator(product,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print('num',page_obj.number)
    context={
        'product':page_obj
    }
    return render(request,'products.html',context)

#searching a specific product
def product_search(request):
    print('Search request received')
    if request.POST:
        print(request.POST)
        # Handle the search query
        search_query = request.POST.get('product_search')
        products_list = products.objects.filter(title__icontains=search_query)
        context = {
            'product': products_list,
            'search_query': search_query
        }
        return render(request, 'products.html', context)
    previous_page = request.META.get('HTTP_REFERER')
    return redirect(previous_page)
    # return redirect('show_page')  # Redirect if not a POST request