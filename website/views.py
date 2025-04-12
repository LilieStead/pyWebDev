from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from website.scraper import get_amazon_product_details
from .models import db, Product

views = Blueprint('views', __name__)

# Landing page route
@views.route('/')
def landing():
    return render_template("landing.html", user=current_user)

# Home page route, only accessible if logged in
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        amazon_link = request.form.get('link')

        if amazon_link:
            # Scrape data from Amazon
            result = get_amazon_product_details(amazon_link)

            # Extract scraped data or set defaults
            title = result.get("title", "No Title")
            price = result.get("price", "N/A")
            description = result.get("description", "No Description")

            # Create a new Product instance
            product = Product(
                link=amazon_link,
                title=title,
                description=description,
                price=price,
                last_price=price,  # Set both prices the same for now
                user_id=current_user.id  # Ensure that the product is linked to the current user
            )

            # Commit to the database
            try:
                db.session.add(product)
                db.session.commit()
                flash("Product added and linked to your account!", category='success')
            except Exception as e:
                db.session.rollback()  # In case of an error, roll back the transaction
                flash(f"Error saving product: {str(e)}", category='error')
        else:
            flash("Please enter a valid Amazon link.", category='error')

    return render_template("home.html", user=current_user)
