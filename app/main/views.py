from flask import Markup, render_template, session, redirect, url_for, flash
from . import main
from .. import db
from .forms import DatasetSubmit, UserSubmit, ContactOwner
from ..models import User, KeyWord, DataSet, Category
from ..email import send_email
from flask.ext.login import login_required, current_user

@main.route('/')
@main.route('/explore/')
#@login_required

def data_share():
    return render_template('datashare.html')

@main.route('/users/')
@login_required
def users_list():
    users = db.session.query(User).all()
    return render_template('users_list.html', users=users)

@main.route('/users_datasets/<int:user_id>/')
@login_required
def users_datasets(user_id):
    this_user = db.session.query(User).filter_by(id=user_id)
    name=this_user.one().fullname
    datasets = this_user.one().dataset
    return render_template('users_datasets.html', user_id=user_id, datasets=datasets, name=name)

@main.route('/keywords_datasets/<int:keyword_id>/')
@login_required
def keywords_datasets(keyword_id):
    keyword = db.session.query(KeyWord).filter_by(id=keyword_id).one()
    name=keyword.keyword
    return render_template('keywords_datasets.html', keyword=keyword, name=name)

@main.route('/categories_datasets/<int:category_id>/')
@login_required
def categories_datasets(category_id):
    this_category = db.session.query(Category).filter_by(id=category_id).one()
    name=this_category.category_name
    return render_template('categories_datasets.html', this_category=this_category, name=name)

@main.route('/keywords/')
@login_required
def keywords_list():
    keywords = db.session.query(KeyWord).all()
    return render_template('keywords_list.html', keywords=keywords)

@main.route('/category/')
@login_required
def categories_list():
    categories = db.session.query(Category).all()
    return render_template('categories_list.html', categories=categories)

@main.route('/dataset/<int:dataset_id>/')
@login_required
def present_dataset(dataset_id):
    dataset = db.session.query(DataSet).filter_by(id=dataset_id).one()
    keywords = ", ".join([keyword.keyword for keyword in dataset.keywords])
    return render_template('present_dataset.html', dataset=dataset, keywords=keywords)

@main.route('/user/<int:user_id>/')
@login_required
def present_user(user_id):
    this_user = db.session.query(User).filter_by(id=user_id).one()
    return render_template('present_user.html', this_user=this_user, user_id=user_id)

@main.route('/register_dataset/', methods=['GET', 'POST'])
@login_required
def register_dataset():
    form = DatasetSubmit()
    this_user = current_user
    username = this_user.fullname
    ## actually adding data to the database
    if form.validate_on_submit():
        ## first we deal with keywords
        list_of_present_keywords = [keyword.keyword for keyword in db.session.query(KeyWord).all()]
        keywords_list_from_form = form.keywords.data.lower().split(",")
        keywords_list_from_form = [keyword.strip() for keyword in keywords_list_from_form]
        ## now construct the list of KeyWord objects
        list_to_append = []
        for keyword in keywords_list_from_form:
            ## if the keyword is not present, create the relevant object
            if not keyword in list_of_present_keywords:
                list_to_append.append(KeyWord(keyword=keyword))
            else:
                ## otherwise relate the existing keyword to the dataset
                list_to_append.append(db.session.query(KeyWord).filter_by(keyword=keyword).one())
        ## now deal with categories
        ## construct the Category object to assign (the same methodology as with keyword)
        list_of_present_categories = [category.category_name for category in db.session.query(Category).all()]
        if form.category.data in list_of_present_categories:
            category_to_assign = db.session.query(Category).filter_by(category_name=form.category.data).first() ### TUTU zmien na all() jak poprawisz baze!
        else:
            category_to_assign = Category(category_name=form.category.data)
        this_user.dataset.append(DataSet(name=form.name.data, numberOfFiles=form.number_of_files.data,
                                         description = form.description.data, category=category_to_assign,
                                         keywords=list_to_append))
        db.session.add(this_user)
        db.session.commit()
        flash("Dataset " +form.name.data+" has been added")
        return redirect(url_for('main.data_share'))
    return render_template('register_dataset.html', form=form, name = username)

# @main.route('/register_user', methods=['GET', 'POST'])
# @login_required
# def register_user():
#     user_id
#     form = UserSubmit()
#     ## actually adding data to the database
#     if form.validate_on_submit():
#         this_user = User(name = form.name.data, fullname = form.fullname.data, email = form.email.data, password = form.password.data)
#         db.session.add(this_user)
#         db.session.commit()
#         flash("User "+form.fullname.data+" has been added")
#         send_email("jaropis@zg.home.pl", "New user added", "mail/new_user", user=this_user.fullname, email=this_user.email)
#         return redirect(url_for('main.data_share', viewer_id=viewer_id))
#     return render_template('register_user.html', form=form)

@main.route('/contact_owner/<int:owner_id>/<int:dataset_id>/', methods=['GET', 'POST'])
@login_required
def contact_owner(owner_id, dataset_id):
    viewer = current_user
    owner = db.session.query(User).filter_by(id=owner_id).one()
    ownername = owner.fullname
    owneremail = owner.email

    viewername = viewer.fullname
    vieweremail = viewer.email

    dataset = db.session.query(DataSet).filter_by(id=dataset_id).one().name

    ##ATTENTION! pre-populating my TextArea with editable 'default' message
    default = 'Hello,\nMy name is '+viewername+'. I found the dataset '+dataset+' on DataShare and I am interested in collaborating.\n Please contact me at '+vieweremail
    form = ContactOwner(content=default)

    if form.validate_on_submit():
        flash("Sent email to "+ownername)
        messagebody_txt = form.content.data
        ## Marking-up to be able to retain html and avoid XSS
        messagebody_html = Markup(form.content.data.replace("\n", "<br>"))
        send_email(owneremail, "Data request", "mail/contact", messagebody_txt=messagebody_txt, messagebody_html=messagebody_html)
        return redirect(url_for('main.data_share'))
    return render_template('contact_form.html', form=form)


