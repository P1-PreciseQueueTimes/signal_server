
from flask_socketio import emit

def handleManualScan(_):

	print("made manual scan")

	emit("manual scan","lol",broadcast=True)

def handleAutomaticScan(_):

	print("made automatic scan")

	emit("automatic scan","lol",broadcast=True)
