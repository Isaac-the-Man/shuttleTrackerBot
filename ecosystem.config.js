module.exports = {
	apps: [
		{
			name: 'ShuttleTrackerBot',
			cwd: '.',
			script: './main.py',
			autorestart: true,
			interpreter: '/usr/bin/python3'
		}
	]
}
