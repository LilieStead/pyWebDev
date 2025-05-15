from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website.scraper import get_amazon_product_details
from .models import db, Product, User  # ✅ Import User
import re
from sqlalchemy.sql.expression import func

views = Blueprint('views', __name__)

@views.route('/')
def landing():
        random_products = Product.query.order_by(func.random()).limit(10).all()
        return render_template("landing.html", user=current_user, products=random_products)

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        amazon_regex = re.compile(r'^(https?:\/\/)?(www\.)?amazon\.(com|co\.uk|de|fr|ca|jp|in|it|es|cn|br|mx|au)\/.+$')
        amazon_link = request.form.get('link')

        if not amazon_link:
            flash("Error: Please enter a valid Amazon link.", category='error')
            return redirect(url_for('views.home'))
        
        if not amazon_regex.match(amazon_link):
            flash("Error: Invalid Amazon link format.", category='error')
            return redirect(url_for('views.home'))

        # Scrape Amazon product details
        result = get_amazon_product_details(amazon_link) or {}
        if result == "notfound":
            flash("Data could not be found", category='error')
            return render_template("home.html", user=current_user)

        if not result or "title" not in result:
            flash("Error: Could not retrieve product details. Ensure the link is valid and points to a product page.", category='error')
            return redirect(url_for('views.home'))

        title = result.get("title", "No Title")
        price = result.get("price", "N/A")
        description = result.get("description", "No Description")

        # Check if product already exists in the database
        existing_product = Product.query.filter_by(link=amazon_link).first()

        if existing_product:
            # Update product details while preserving previous price
            existing_product.last_price = existing_product.price  # Preserve the previous price before updating
            existing_product.price = price
            existing_product.title = title
            existing_product.description = description

            # Check if the user is already linked to this product in the association table
            if existing_product not in current_user.products:
                current_user.products.append(existing_product)  # Only add relationship if not already linked
        else:
            # Create new product entry
            new_product = Product(
                link=amazon_link,
                title=title,
                description=description,
                price=price,
                last_price=price  # Initially same as price since it's new
            )

            db.session.add(new_product)

            # Establish user-product relationship ONLY if it doesn’t already exist
            if new_product not in current_user.products:
                current_user.products.append(new_product)

        try:
            db.session.commit()
            flash("Success: Product updated or added, and linked to your account!", category='success')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: Could not save product. {str(e)}", category='error')

        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)
