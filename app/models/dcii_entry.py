from .. import db

class DCIIEntry(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)

    subjects = db.relationship('DCIISubject', back_populates='entry', cascade='all, delete-orphan')
    
    @property
    def get_last_index(self):
        highest_index = 0
        for subject in self.subjects:
            if subject.index > highest_index:
                highest_index = subject.index
        return highest_index + 1

class DCIISubject(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    index = db.Column('index', db.Integer)
    classification_type = db.Column('cls_type', db.String, nullable=False)
    classification_tags = db.Column('cls_tags', db.String, nullable=False)
    classification_qualifier = db.Column('cls_qualifier', db.String, nullable=False)
    
    containment_status = db.Column('cnt_status', db.String, nullable=False)
    containment_tags = db.Column('cnt_tags', db.String, nullable=False)
    
    danger = db.Column('danger', db.String, nullable=False)
    probability = db.Column('probability', db.String, nullable=False)
    
    clearance = db.Column('clearance', db.Integer)
    
    body = db.Column('body', db.Text, nullable=False)
    
    entry_id = db.Column(db.Integer, db.ForeignKey('dcii_entry.id'), nullable=False)
    entry = db.relationship('DCIIEntry', back_populates='subjects')
    addons = db.relationship('DCIIAddon', back_populates='subject', cascade='all, delete-orphan')
    
    @property
    def get_last_index(self):
        highest_index = 0
        for addon in self.addons:
            if addon.index > highest_index:
                highest_index = addon.index
        return highest_index + 1

class DCIIAddon(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    index = db.Column('index', db.Integer)
    
    addon_type = db.Column('adn_type', db.String)
    
    body = db.Column('body', db.Text)
    
    subject_id = db.Column(db.Integer, db.ForeignKey('dcii_subject.id'), nullable=False)
    subject = db.relationship('DCIISubject', back_populates='addons')
