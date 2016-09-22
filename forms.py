from wtforms import Form, BooleanField, StringField, validators, DateTimeField, TextAreaField, \
    IntegerField, SelectField


class RegistrationForm(Form):
    username     = StringField('Username', [validators.Length(min=4, max=25)])
    email        = StringField('Email Address', [validators.Length(min=6, max=35)])

class ProfileForm(Form):
    birthday  = DateTimeField('Your Birthday', format='%m/%d/%y')
    signature = TextAreaField('Forum Signature')

class AdminProfileForm(ProfileForm):
    username = StringField('Username', [validators.Length(max=40)])
    level    = IntegerField('User Level', [validators.NumberRange(min=0, max=10)])

class RequirementDropDown(Form):
    NeedsDropDown = SelectField(u'FIND A NEED', choices=[('0', 'BUSINESS NEED'), ('1', 'DELIVERABLE'), ('2', 'SOLUTION')],
                                                         coerce = unicode, default = '0')
    BusDropDown = SelectField(u'BUSINESS NEED', choices=[('0', 'Brainstorming'), ('1', 'Collaboration'), ('2', 'Communication'),
                                                         ('3', 'Coordination'), ('4', 'Decision')],
                              coerce=unicode, default='0')
    DelDropDown = SelectField(u'DELIVERABLE', choices=[('0', 'Deliver A'), ('1', 'Deliver B')], coerce=unicode, default='0')