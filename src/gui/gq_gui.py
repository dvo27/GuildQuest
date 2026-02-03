from models import Campaign, User

class gq_GUI:
    def __init__(self, given_campaign: Campaign, selected_user: User):
        self.given_campaign = given_campaign
        self.selected_user = selected_user
        
    def show_text_display(self) -> None:
        pass
    
    def show_classic_display(self) -> None:
        pass