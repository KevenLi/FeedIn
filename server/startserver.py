import os
import feeding.engine
import feeding.model
import time
import elasticsearch
import uuid

if __name__ == '__main__':
    root = './feeds'
    jobs = []
    engine = feeding.engine.Engine()
    es = elasticsearch.Elasticsearch()
    for dir in os.listdir(root):
        dir_path = os.path.join(root, dir) 
        if os.path.exists(os.path.join(dir_path, 'feed.xml')):
            feed_setting_file = os.path.join(dir_path, 'feed.xml')
            print 'loaded feed', feed_setting_file
            job = engine.create(feed_setting_file)
            jobs.append(job)
    
    while True:
        for job in jobs:
            context = feeding.model.Context()
            job.execute(context)
            
            for item in context.items:
                item_body = item

                # assign id
                if not '_id' in item_body:
                    item_body['_id'] = str(uuid.uuid4())
                
                # assign timestamp
                timestamp = time.localtime()
                item_body['_ts'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', timestamp)

                # submit index                
                es.index('guba', 'thread', item_body, item_body['_id'])
                print item.text('url')
        time.sleep(10)