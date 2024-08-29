from bs4 import BeautifulSoup
import requests
import re


class SCP:
    def __init__(self, number, name, site, cont_class, disr_class, risk_class, image):
        self.number = number
        self.name = name
        self.site = site
        self.containment_class = cont_class
        self.disruption_class = disr_class 
        self.risk_class = risk_class
        self.image = image 

    def __str__(self):
        return (f"SCP-{self.number}\n"
                f"Site: {self.site}\n"
                f"Containment Class: {self.containment_class}\n"
                f"Disruption Class: {self.disruption_class}\n"
                f"Risk Class: {self.risk_class}\n"
                f"Image: {self.image}")
    @staticmethod
    def create_scp(num):
        url = f'https://scp-wiki.wikidot.com/scp-{num}'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        
        txt = "\n".join(soup.text.splitlines()[219:])
        """
        with open("text.txt","w",encoding="utf-8") as f:
            f.write(html)
        """
        number = num

        # check if there's a containment site
        site_search = re.search(r"Site-\s*([^\n]+)", txt)
        site = site_search.group(1).strip() if site_search else None

        # find class (keter, euclid, safe)
        cont_class_search = re.search(r"(Containment Class|Object Class):\s*([^\n]+)", txt)
        cont_class = cont_class_search.group(2).strip() if cont_class_search else None

        # get disruption class (dark, vlam, notice)
        disr_class_search = re.search(r"Disruption Class:\s*([^\n]+)", txt)
        disr_class = disr_class_search.group(1).strip() if disr_class_search else None

        # get risk class (notice, caution, warning)
        risk_class_search = re.search(r"Risk Class:\s*([^\n]+)", txt)
        risk_class = risk_class_search.group(1).strip() if risk_class_search else None

        # find all image divs
        image_divs = soup.find_all('div', class_='scp-image-block')
        if image_divs:
            images = []
            # check in the divs for images and descriptions
            for x in image_divs:
                image = x.find('img')["src"]
                img_desc = x.find('div').find('p')
                images.append([image, img_desc.text])
        else: images = None

        return SCP(number=num, name=None, site=site, cont_class=cont_class, disr_class=disr_class, risk_class=risk_class, image=images)