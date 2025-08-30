// Sample paper data (mock data)
const paperData = [
    // { id: 1, course: 'btech', session: '2023', subject: 'Data Structures', name: 'B.Tech Data Structures Mid-Term 2023', file: '#' },
    // { id: 2, course: 'btech', session: '2022', subject: 'Database Management', name: 'B.Tech DBMS Final Exam 2022', file: '#' },
    // { id: 3, course: 'mtech', session: '2023', subject: 'Machine Learning', name: 'M.Tech Machine Learning End-Term 2023', file: '#' },
    // { id: 4, course: 'bsc', session: '2021', subject: 'Physics', name: 'B.Sc Physics Final Exam 2021', file: '#' }
];

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
    const courseSelect = document.getElementById('courseSelect');
    const sessionSelect = document.getElementById('sessionSelect');
    const subjectInput = document.getElementById('subjectInput');
    const semesterInput = document.getElementById('semesterInput');
    const searchBtn = document.getElementById('searchBtn');
    const noResults = document.getElementById('noResults');
    const paperResults = document.getElementById('paperResults');

    // Store the API data globally for search functionality
    let allPapers = [];
    
    // Fetch data from API
    const url = '/api/resources/'
    fetch(url)
    .then(res => res.json())
    .then(data => {
        allPapers = data.data;
        console.log('Loaded papers:', allPapers);
        
        // Display all papers initially
        displayPapers(allPapers);
    }).catch(err => {
        console.log('Error fetching data:', err);
        noResults.style.display = 'block';
        noResults.textContent = 'Error loading papers. Please try again later.';
    });
    
    // Function to display papers
    function displayPapers(papers) {
        if(papers && papers.length > 0) {
            // Hide the no results message
            noResults.style.display = 'none';
            // Show the results container
            paperResults.style.display = 'flex';
            // Clear any existing results
            paperResults.innerHTML = '';
            
            papers.forEach(paper => {
                const paperCard = document.createElement('div');
                paperCard.className = 'col-md-6 col-lg-4 mb-4';
               paperCard.innerHTML = `
                    <div class="paper-card card shadow-sm border-0 rounded-3 mb-4">
                        <div class="card-body">
                            <!-- Header -->
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <h5 title='${paper.name}' class="card-title mb-0 fw-semibold text-truncate">${paper.name}</h5>
                                <span class="badge bg-primary-subtle text-primary fw-semibold">${paper.session}</span>
                            </div>

                            <!-- Details -->
                            <ul class="list-unstyled small text-muted mb-3">
                                <li><strong>📘 Course:</strong> ${paper.course.toUpperCase()}</li>
                                <li><strong>📖 Subject:</strong> ${paper.subject}</li>
                                <li><strong>📖 Semester:</strong> ${paper.semester}</li>
                            </ul>
                             <div class="mb-3">
                                    <small class='text-sm'>by ${paper.created_by}</small>
                                </div>

                            <!-- Tags -->
                                <div class="mb-3">
                                    ${paper.tags.map(tag => `
                                        <span class="badge bg-light text-dark border me-1 mb-1">#${tag.name}</span>
                                    `).join('')}
                                </div>

                            <!-- Download Button -->
                            <div class="d-grid">
                                <a href="${paper.url || paper.file}" target='blank_'
                                class="btn btn-danger fw-semibold rounded-pill">
                                ⬇ Download
                                </a>
                            </div>
                        </div>
                    </div>
                `;
                                                      


                paperResults.appendChild(paperCard);
            });
        } else {
            // If no data, show the no results message
            noResults.style.display = 'block';
            noResults.textContent = 'No papers found matching your criteria.';
            paperResults.style.display = 'none';
        }
    }
    
    // Search functionality
    searchBtn.addEventListener('click', function() {
        const course = courseSelect.value;
        const session = sessionSelect.value;
        const subject = subjectInput.value.toLowerCase();
        const semester = semesterInput.value;
        console.log('Search criteria:', course, session, subject,semester);
        
        const url_ = `/api/resources/?course=${course}&session=${session}&semester=${semester}&subject=${subject}`
        fetch(url_, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            displayPapers(data.data);
        })
        .catch(err => {
            console.log(err);
        })
    
    });
    
    // Add hover effects to buttons and cards
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

console.log("test")