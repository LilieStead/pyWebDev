from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from website.scraper import get_amazon_product_details
from .models import db, Product
import re
from flask import redirect, url_for

views = Blueprint('views', __name__)

# Landing page route
@views.route('/')
def landing():
    return render_template("landing.html", user=current_user)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        amazon_regex = re.compile(r'^(https?:\/\/)?(www\.)?amazon\.(com|co\.uk|de|fr|ca|jp|in|it|es|cn|br|mx|au)\/.+$')
        amazon_link = request.form.get('link')

        if not amazon_link:
            flash("Error: Please enter a valid Amazon link.", category='error')
            return redirect(url_for('views.home'))  # **Ensure redirect prevents stacked errors**
        
        if not amazon_regex.match(amazon_link):
            flash("Error: Invalid Amazon link format.", category='error')
            return redirect(url_for('views.home'))  # **Redirect instead of rendering template**

        # Scrape Amazon product details
        result = get_amazon_product_details(amazon_link) or {}
        if result == "notfound":
            flash(f"data could not be found", category='error')
            return render_template("home.html", user=current_user)

        if not result or "title" not in result:
            flash("Error: Could not retrieve product details. Ensure the link is valid and points to a product page.", category='error')
            return redirect(url_for('views.home'))  # **Redirect for error instead of rendering**

        # Extract product data with fallbacks
        title = result.get("title", "No Title")
        price = result.get("price", "N/A")
        description = result.get("description", "No Description")

        # Store in database
        product = Product(
            link=amazon_link,
            title=title,
            description=description,
            price=price,
            last_price=price,
            user_id=current_user.id
        )

        try:
            db.session.add(product)
            db.session.commit()
            flash("Success: Product added and linked to your account!", category='success')
            return redirect(url_for('views.home'))  # **Redirect ensures fresh data load**
        except Exception as e:
            db.session.rollback()
            flash(f"Error: Could not save product. {str(e)}", category='error')
            return redirect(url_for('views.home'))  # **Redirect after rollback**

    return render_template("home.html", user=current_user)