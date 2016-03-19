from app import db
from app.models import User, KeyWord, DataSet


keywords_list_from_form = []
list_of_present_keywords = [keyword.keyword for keyword in db.session.query(KeyWord).all()]
### collecting keywords with spaces
for keyword in list_of_present_keywords:
    if keyword != keyword.strip():
        keywords_list_from_form.append(keyword)
for keyword in keywords_list_from_form:
    ### for keywords that are represented only by the version with space
    if keyword.strip() not in list_of_present_keywords and keyword in list_of_present_keywords:
        datasets = db.session.query(DataSet).filter(keyword in db.session.query(DataSet)).all()
        new_keyword = db.session.query(KeyWord).filter_by(keyword=keyword.strip()).one()
        for dataset in datasets:
            dataset.keyword=new_keyword
            db.session.add(dataset)
            to_delete = db.session.query(KeyWord).filter_by(keyword=keyword)
            db.session.delete(to_delete)
    ### for keywords that are present both as stripped and as keyword_with_space
    if keyword.strip() in list_of_present_keywords and keyword in list_of_present_keywords:
        datasets = db.session.query(DataSet).filter_by(keyword=keyword).all()
        new_keyword = db.session.query(KeyWord).filter_by(keyword=keyword.strip()).one()
        for dataset in datasets:
            dataset.keyword=new_keyword
            db.session.add(dataset)
            to_delete = db.session.query(KeyWord).filter_by(keyword=keyword)
            db.session.delete(to_delete)

list_of_present_keywords = [keyword.keyword for keyword in db.session.query(KeyWord).all()]
print list_of_present_keywords
