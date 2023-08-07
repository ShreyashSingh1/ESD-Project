from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# In-memory data for demonstration purposes
job_listings = []

# Define a Job class
class Job:
    def __init__(self, title, location, job_type, industry):
        self.title = title
        self.location = location
        self.job_type = job_type
        self.industry = industry

# Routes for web pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/job/<int:job_id>')
def job_listing(job_id):
    job = job_listings[job_id]  # Assume job_listings is a list of Job objects
    return render_template('job_listing.html', job=job, job_id=job_id)

@app.route('/apply/<int:job_id>')
def apply(job_id):
    job = job_listings[job_id]  # Assume job_listings is a list of Job objects
    return render_template('apply.html', job=job, job_id=job_id)

# API routes
@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job = Job(data['title'], data['location'], data['job_type'], data['industry'])
    job_listings.append(job)
    return jsonify({'message': 'Job created successfully'}), 201

@app.route('/api/jobs', methods=['GET'])
def search_jobs():
    location = request.args.get('location')
    job_type = request.args.get('job_type')
    industry = request.args.get('industry')
    
    filtered_jobs = []
    
    for idx, job in enumerate(job_listings):
        if (not location or location == job.location) and \
           (not job_type or job_type == job.job_type) and \
           (not industry or industry == job.industry):
            filtered_jobs.append({
                'id': idx,
                'title': job.title,
                'location': job.location,
                'job_type': job.job_type,
                'industry': job.industry
            })
    
    return jsonify(filtered_jobs), 200

if __name__ == '__main__':
    app.run(host = "0.0.0.0")
