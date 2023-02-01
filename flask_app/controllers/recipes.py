from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from flask_app.models.recipe import User

@app.route('/add/recipe', methods = ['POST'])
def add_recipe():
    if 'user_id' not in session:
        return redirect('/')
    
    if not Recipe.save_recipe(request.form):
        return redirect('/create/recipe')
    else:
        return redirect('/user/home')

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    data = {
        'id' : id
    }
    Recipe.delete_recipe(data)
    return redirect('/user/home')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')

    data = {
        'id' : id
    }
    user = {
        'id': session['user_id']
    }

    return render_template('recipes/edit_recipe.html', recipe = Recipe.get_by_id(data), user = User.get_by_id(user))

@app.route('/update/recipe/<int:id>', methods = ['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/recipe/{id}')

    data = {
        'id' : id,
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instructions' : request.form['instructions'],
        'date_made' : request.form['date_made'],
        'under' : request.form['under'],
    
    }
    Recipe.update(data)
    return redirect('/user/home')
        
    
    



@app.route('/recipe/view/<int:id>')
def view_recipe(id):
    data = {
        'id' : id,
    }
    user = {
        'id': session['user_id']
    }
    return render_template('recipes/view_recipe.html', recipe = Recipe.get_by_id(data), user = User.get_by_id(user))