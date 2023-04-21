from difflib import get_close_matches
from flaskr.tag_handler import TagHandler
from google.cloud import storage
from flask import abort
from bleach import Cleaner
import hashlib
import folium
from folium import plugins
import html.parser


class Backend:

    def __init__(self, storage_client=storage.Client()):
        # Solution Storage: uses storage client to make buckets that are
        # essentially hidden from the frontend
        self.page_bucket = storage_client.bucket("wiki_content_p1")
        self.login_bucket = storage_client.bucket("users_passwords_p1")
        self.image_bucket = storage_client.bucket("developer_images")

    def get_wiki_page(self, name):  #wiki_content_p1
        blob_name = name
        # Solution code: uses page_bucket and checks for None value
        blob = self.page_bucket.blob(blob_name)
        if blob is None:
            return None
        return blob.download_as_text()

    def get_all_page_names(self):
        self.pages = []
        # Solution code: uses page bucket and doesn't list image files
        for blob in self.page_bucket.list_blobs():
            if not blob.name.endswith(("png", "jpg", "jpeg", "csv")):
                self.pages.append(blob.name)
        return self.pages

    def upload(self, file, name, original_filename):
        bucket = self.page_bucket
        if (original_filename.endswith(("png", "jpg", "jpeg"))):
            bucket = self.image_bucket
        blob = bucket.blob(name)
        if blob.exists():
            blob.delete()
        with blob.open("wb") as f:
            f.write(file)

    def is_valid_html(self, html):
        """Checks if the given HTML string is safe.

        Args:
            html: A string containing HTML code.

        Returns:
            True if the HTML is safe, False otherwise.
        """
        cleaner = Cleaner(tags=[
            'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'title',
            'div', 'em', 'i', 'li', 'ol', 'p', 'strong', 'u', 'ul', 'img'
        ],
                          attributes={
                              'a': ['href', 'title'],
                              'abbr': ['title'],
                              'acronym': ['title'],
                              'img': ['src', 'alt']
                          })

        sanitized_html = cleaner.clean(html)

        if sanitized_html != html:
            return False
        return True

    def tree_map(self):
        tree_distributions = {
            'Coast Redwood': {
                'location': (38.9822, -123.3781),
                'distribution': 'North America',
                'color': 'green'
            },
            'Ginko': {
                'location': (39.7684, -86.1581),
                'distribution': 'East Asia',
                'color': 'red'
            },
            'Japanese Magnolia': {
                'location': (35.8801, -79.0800),
                'distribution': 'East Asia',
                'color': 'blue'
            },
            'Juniper': {
                'location': (40.7968, -77.8619),
                'distribution': 'North America, Eurasia',
                'color': 'orange'
            },
            'Live Oak': {
                'location': (30.3894, -86.5229),
                'distribution': 'North America',
                'color': 'darkgreen'
            },
            'Monterey Cypress': {
                'location': (36.6002, -121.8947),
                'distribution': 'North America',
                'color': 'darkblue'
            },
            'Palm': {
                'location': (26.7056, -80.0364),
                'distribution': 'Africa, Eurasia, Americas',
                'color': 'pink'
            },
            'Palmetto': {
                'location': (26.7153, -81.0522),
                'distribution': 'North America',
                'color': 'darkred'
            },
            'Water Oak': {
                'location': (30.4383, -84.2807),
                'distribution': 'North America',
                'color': 'gray'
            },
            'White Oak': {
                'location': (33.9860, -83.7185),
                'distribution': 'North America',
                'color': 'purple'
            }
        }

        tree_names = [
            'Coast Redwood', 'Ginko', 'Japanese Magnolia', 'Juniper',
            'Live Oak', 'Monterey Cypress', 'Palm', 'Palmetto', 'Water Oak',
            'White Oak'
        ]

        tree_map = folium.Map(location=[39.8283, -98.5795], zoom_start=5)

        for i, tree in enumerate(tree_names):
            description = "<b style='font-size: 16px;'>Distribution: </b><h style='font-size: 16px;'>{}</h>".format(
                tree_distributions[tree]['distribution'])
            popup_html = '<b>{}</b><br>{}<br><a href="#" onclick="window.top.location.href=\'/pages/{}\'; return false;">Learn More</a>'.format(
                tree, description, tree)
            folium.Marker(
                location=tree_distributions[tree]['location'],
                icon=folium.Icon(color=tree_distributions[tree]['color'],
                                 icon='leaf',
                                 prefix='fa'),
                popup=popup_html,
                tooltip=tree,
            ).add_to(tree_map)

        legend_html = '''
                    <div style="position:fixed; 
                            bottom: 50px; left: 50px; width: 160px; height: 300px; 
                            border:2px solid grey; z-index:9999; font-size:14px;
                            background-color:rgba(255, 255, 255, 0.8);">
                    <h4 style="text-align:center; margin-top:10px;">Legend:</h4>
                    <table style="margin-left:auto; margin-right:auto;">
                        &nbsp; Legend: <br>
                '''
        for i in range(len(tree_names)):
            legend_html += f'<tr><td><i style="background-color:{tree_distributions[tree_names[i]]["color"]}; border-radius:50%; width:10px; height:10px; display:inline-block;"></i></td><td style="padding-left:8px;">{tree_names[i]}</td></tr>'

        legend_html += '''
                </table>
            </div>
            '''
        tree_map.get_root().html.add_child(folium.Element(legend_html))
        map_html = tree_map._repr_html_()
        return map_html

    def sign_up(self, username, password):
        blob = self.login_bucket.blob(f"users/{username}")
        # blob = self.bucket.blob(username)
        if blob.exists():
            return False

        # Hash password
        hash_pword = hashlib.blake2b(password.encode()).hexdigest()

        user_blob = {"username": username, "hash_pword": hash_pword}
        blob.upload_from_string(str(user_blob))

        return True

    def sign_in(self, username, password):
        blob = self.login_bucket.blob(f"users/{username}")
        # blob = self.bucket.blob(username)
        if not blob.exists():
            return False

        get_pword = blob.download_as_bytes()
        get_pword = eval(get_pword)
        user_pword = hashlib.blake2b(password.encode()).hexdigest()

        if get_pword["hash_pword"] == user_pword:
            return True
        else:
            return False

    def get_image(self, image_name):
        # Solution code: check for if blob is none
        blob = self.image_bucket.get_blob(image_name)
        if blob is None:
            return bytearray()

        with blob.open("rb") as image:
            f = image.read()
            b = bytearray(f)
            return b

    def search(self, search_input):
        # Uses the difflib Python library(specifically the “get_close_matches” function)
        # to return page results that might be spelled incorrectly.
        tag_handler = TagHandler()
        return set(
            get_close_matches(search_input, self.get_all_page_names()) +
            tag_handler.get_filenames_by_tag(search_input))
