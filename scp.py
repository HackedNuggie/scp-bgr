from bs4 import BeautifulSoup
import requests
import re


class SCP:
    def __init__(self, number, description, site, cont_class, disr_class, risk_class, image):
        self.number = number
        self.description = description
        self.site = site
        self.containment_class = cont_class
        self.disruption_class = disr_class 
        self.risk_class = risk_class
        self.image = image 

    def __str__(self):
        return (f"SCP-{self.number}\n"
                f"Contained in: {self.site}\n"
                f"Containment Class: {self.containment_class}\n"
                f"Disruption Class: {self.disruption_class}\n"
                f"Risk Class: {self.risk_class}\n"
                f"Description: {self.description}\n"
                f"Image: {self.image}")
    
    def json(self):
        return {
            "number": self.number,
            "site": self.site,
            "containment_class": self.containment_class,
            "disruption_class": self.disruption_class,
            "risk_class": self.risk_class,
            "description": self.description,
            "image": self.image
        }

    @staticmethod
    def create_scp(num):
        url = f'https://scp-wiki.wikidot.com/scp-{num}'
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        
        txt = "\n".join(soup.text.splitlines()[215:])
        """
        with open("text.txt","w",encoding="utf-8") as f:
            f.write(txt)
        """
        number = num

        # check if there's a containment site
        #site_search = re.search(r'(?:contained|located|held|housed|situated|stored|kept|occupies|placed)\s+(?:in|on|at|a|within|by|near|adjacent to|around)\s+(.*)', txt) # I might be a dumbass
        site_search = re.search(r'(?:Special Containment Procedures:|Special Containment Procedure:|Special Containment Procedures|Special Containment Procedure)\s*([^\n]+)', txt, re.IGNORECASE)
        site = site_search.group(1).strip() if site_search else None


        desc_search = re.search(r"(?:description:|description )\s*([^\n]+)", txt, re.IGNORECASE)
        desc = desc_search.group(1).strip() if desc_search else None
        # find class (keter, euclid, afe)
        cont_class_search = re.search(r"(Containment Class|Object Class):\s*([^\n]+)", txt, re.IGNORECASE)
        cont_class = cont_class_search.group(2).strip() if cont_class_search else None

        # get disruption class (dark, vlam, notice)
        disr_class_search = re.search(r"Disruption Class:\s*([^\n]+)", txt, re.IGNORECASE)
        disr_class = disr_class_search.group(1).strip() if disr_class_search else None
        
        # get risk class (notice, caution, warning)
        risk_class_search = re.search(r"Risk Class:\s*([^\n]+)", txt, re.IGNORECASE)
        risk_class = risk_class_search.group(1).strip() if risk_class_search else None

        # find all image divs
        image_divs = soup.find_all('div', class_='scp-image-block')
        if image_divs:
            images = []
            # check in the divs for images and descriptions
            for x in image_divs:
                image = x.find('img')["src"]
                img_desc = x.find('div').find(['p','tt'])
                images.append([image, img_desc.text])
        else: images = None

        return SCP(number=num, description=desc, site=site, cont_class=cont_class, disr_class=disr_class, risk_class=risk_class, image=images)