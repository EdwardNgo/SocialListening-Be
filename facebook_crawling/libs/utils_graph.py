from datetime import datetime
access_token = 'EAAAAZAw4FxQIBAPhEjmWzk0xgkk4cqnS2VWr7mtgh5cEEA552QVNdobUe59nZCZCoyHGuCUZAcuFyfoWe0BYKA1bBtsZAhCF457gQH3O3H8FFtIk3fi3YzY35EYhMq12bn6AqQn5yoce3vtNOTsAueafUqnEZAlTn23fKJZBcWkAgZDZD'

InsertPost_1 = """mutation MyMutation($post_id: String, $content: String, $created_at: String,$img_link:String,$page_id:String) {
        insert_posts(objects: {
            img_link: $img_link,
            created_at: $created_at,
            content: $content,
            post_id: $post_id,
            page_id: $page_id,

            }) {
            __typename
        }
        }"""
bulkInsertPost = """mutation MyMutation($objects: posts_insert_input ) {
        insert_posts(objects: {
            objects: $objects
            }) {
            __typename
        }
        }"""

def dateToSecond(date):
    dateFormat = date.split('T')[0]
    date_time_obj = datetime.strptime(dateFormat, '%Y-%m-%d')
    b = datetime(1970, 1, 1)

    return str(int((date_time_obj-b).total_seconds()))