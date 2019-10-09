"""this class can be used to get gists, listing out gists, gist id, edit gist, delete gist from Github account
need to call this class with user name of github account 
ex gist(user = "<userName>")
"""

import json
import requests

BASE_URL = 'https://api.github.com'
GIST_URL = 'https://gist.github.com'

class gist:

    def __init__(self, **args):
        if 'user' in args:
            self.user = args['user']
        # else:
        #     self.user = self.gist.username

    def list_all_gists(self):
        file_name = []
        r = requests.get('%s/users/%s/gists' % (BASE_URL, self.user))
        print('%s/users/%s/gists' % (BASE_URL, self.user))
        print(r.json())
        r_text = json.loads(r.text)
        limit = len(r.json())
        if (r.status_code == 200):
            for g,no in zip(r_text,range(0,limit)):
                for key,value in r.json()[no]['files'].items():
                    # print(file_name.append(value['filename']))
                    file_name.append(value['filename'])
            return file_name
        raise Exception("username not found")

    def get_gist_ID(self, gistName):
        file_name =[]
        r = requests.get('%s/users/%s/gists' % (BASE_URL, self.user))
        print('%s/users/%s/gists' % (BASE_URL, self.user))
        r_text = json.loads(r.text)
        limit = len(r.json())
        if (r.status_code == 200):
            for g,no in zip(r_text, range(0, limit)):
                for key, value in r.json()[no]['files'].items():
                    if str(value['filename']) == str(gistName):
                        return r.json()[no]['id']
        return 0

    def get_gist_content(self, **kwargs):
        self.gist_name = ''
        if 'name' in kwargs:
            self.gist_name = kwargs['name']
            self.gist_id = self.get_gist_ID(self.gist_name)
        elif 'id' in kwargs:
            self.gist_id = kwargs['id']
        else:
            raise Exception('Either provide authenticated user\'s Unambigious Gistname or any unique Gistid')
        print(self.gist_id)
        if self.gist_id:
            r = requests.get('%s'%BASE_URL+'/gists/%s' %self.gist_id)
            print(r.json())
            if (r.status_code == 200):
                r_text = json.loads(r.text)
                if self.gist_name!='':
                    content =  r.json()['files'][self.gist_name]['content']
                else:
                    for key,value in r.json()['files'].items():
                        content = r.json()['files'][value['filename']]['content']
                return content
            raise Exception('No such gist found')

    def getgist(self, **args):
        if 'id' in args:
            self.gist_id = args['id']
        else:
            raise Exception('Gist ID must be provided')
        if self.gist_id:
            r = requests.get('%s/gists/%s'%(BASE_URL,self.gist_id))
            if (r.status_code == 200):
                for key,value in r.json()['files'].iteritems():
                    content = value['filename']
                return content

        raise Exception('No such gist found')

    def edit(self, **args):
		'''
		Doesn't require manual fetching of gistID of a gist
		passing gistName will return edit the gist
		'''
        self.gist_name = ''
        if 'description' in args:
            self.description = args['description']
        else:
            self.description = ''

        if 'name' in args and 'id' in args:
            self.gist_name = args['name']
            self.gist_id = args['id']
        elif 'name' in args:
            self.gist_name = args['name']
            self.gist_id = self.getMyID(self.gist_name)
        elif 'id' in args:
            self.gist_id = args['id']
        else:
            raise Exception('Gist Name/ID must be provided')

        if 'content' in args:
            self.content = args['content']
        else:
            raise Exception('Gist content can\'t be empty')

        if (self.gist_name == ''):
            self.gist_name = self.getgist(id=self.gist_id)
            data = {"description": self.description,"files": {self.gist_name: {"content": self.content}}}
        else:
            data = {"description": self.description,"files": {self.gist_name: {"content": self.content}}}

        if self.gist_id:
            r = requests.patch('%s/gists/%s'%(BASE_URL,self.gist_id),data=json.dumps(data))
            if (r.status_code == 200):
                r_text = json.loads(r.text)
                response = {'updated_content': self.content, 'created_at': r.json()['created_at'],'comments':r.json()['comments']}
                return response
        raise Exception('No such gist found')

	def delete(self, **args):
		'''
		Delete a gist by gistname/gistID
		'''
        if 'name' in args:
            self.gist_name = args['name']
            self.gist_id = self.getMyID(self.gist_name)
        elif 'id' in args:
            self.gist_id = args['id']
        else:
            raise Exception('Provide GistName to delete')

        url = 'gists'
        if self.gist_id:
            r = requests.delete('%s/%s/%s'%(BASE_URL,url,self.gist_id))
            if (r.status_code == 204):
                response = {'id': self.gist_id}
                return response
            raise Exception('Can not delete gist')

	def starred(self, **args):
        '''List the authenticated user's starred gists'''
        ids =[]
        r = requests.get('%s/gists/starred'%BASE_URL)
        if 'limit' in args:
            limit = args['limit']
        else:
            limit = len(r.json())

        if (r.status_code == 200):
            for g in range(0,limit ):
                ids.append('%s/%s/%s' %(GIST_URL,r.json()[g]['user']['login'],r.json()[g]['id']))
            return ids

        raise Exception('Username not found')

    def links(self,**args):
        '''Return Gist URL-Link, Clone-Link and Script-Link to embed'''

        if 'name' in args:
            self.gist_name = args['name']
            self.gist_id = self.getMyID(self.gist_name)
        elif 'id' in args:
            self.gist_id = args['id']
        else:
            raise Exception('Gist Name/ID must be provided')
        if self.gist_id:
            r = requests.get('%s/gists/%s'%(BASE_URL,self.gist_id))
            if (r.status_code == 200):
                content = {
                'Github-User': r.json()['user']['login'],
                'GistID': r.json()['id'],
                'Gist-Link': '%s/%s/%s' %(GIST_URL,self.user,r.json()['id']),
                'Clone-Link': '%s/%s.git' %(GIST_URL,r.json()['id']),
                'Embed-Script': '<script src="%s/%s/%s.js"</script>' %(GIST_URL,self.user,r.json()['id'])
                }
                return content

        raise Exception('No such gist found')

g = gist(user = 'CNG51')
out = g.get_gist_content(name = 'some.py')
print("printing outpuuuut")
print(out)
