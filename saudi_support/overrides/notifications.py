
import frappe
from frappe import _
from frappe.email.doctype.notification.notification import Notification, get_context, json
import requests

class ERPGulfNotification(Notification): 
    
    def validate(self):
        self.validate_saudi_support_settings()
        super(ERPGulfNotification, self).validate()
    
    def validate_saudi_support_settings(self):
        settings = frappe.get_doc('Saudi Support Configuration')
        if self.enabled and self.channel == 'Saudi Support WhatsApp':
            if not settings.access_token or not settings.api_url or not settings.instance_id:
                frappe.throw(_("Please configure Saudi Support WhatsApp settings to send WhatsApp messages"))
            
    def send(self, doc):
        context = get_context(doc)
        context = {"doc": doc, "alert": self, "comments": None}
        if doc.get("_comments"):
            context["comments"] = json.loads(doc.get("_comments"))

        if self.is_standard:
            self.load_standard_properties(context)
            
        try:
            if self.channel == "Saudi Support WhatsApp":
                self.send_whatsapp_msg(doc, context)
        except:
            frappe.log_error(title='Failed to send notification', message=frappe.get_traceback())
        super(ERPGulfNotification, self).send(doc)
        
    
    def send_whatsapp_msg(self, doc, context):
        settings = frappe.get_doc('Saudi Support Configuration')
        recipients = self.get_receiver_list(doc, context)
        receiverNumbers = []
        for receipt in recipients:
            number = receipt
            if "{" in number:
                number = frappe.render_template(receipt, context)
            message=frappe.render_template(self.message, context)        
            phoneNumber = self.get_receiver_phone_number(number)
            receiverNumbers.append(phoneNumber)
            url = f"{settings.api_url}/send"
            headers = {'Content-type': 'application/json'}
            data = {'number': phoneNumber, "type": "text", "message": message, "instance_id": settings.instance_id,
                    "access_token": settings.access_token}
            response = requests.post(url, data= json.dumps(data), headers=headers)
            #frappe.msgprint("This is an Error Message" + response.text)
        #frappe.msgprint('Document updated successfully ' + response.text)
    
    def get_receiver_phone_number(self, number):
        phoneNumber = number.replace("+","").replace("-","")
        if phoneNumber.startswith("+") == True:
            phoneNumber = phoneNumber[1:]
        elif phoneNumber.startswith("00") == True:
            phoneNumber = phoneNumber[2:]
        elif phoneNumber.startswith("0") == True:
            if len(phoneNumber) == 10:
                phoneNumber = "966" + phoneNumber[1:]
        else:
            if len(phoneNumber) < 10: 
                phoneNumber ="966" + phoneNumber
        if phoneNumber.startswith("0") == True:
            phoneNumber = phoneNumber[1:]
        
        return phoneNumber   