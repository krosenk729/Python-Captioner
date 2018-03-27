from django import template

register = template.Library()

@register.simple_tag
def user_did_upvote(u_votes, user):
	user_vote = 0
	for v in u_votes:
		if v.user == user:
			user_vote = v.value
	return "voted" if user_vote > 0 else ""

@register.simple_tag
def user_did_downvote(u_votes, user):
	user_vote = 0
	for v in u_votes:
		if v.user == user:
			user_vote = v.value
	return "voted" if user_vote < 0 else ""
