document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('curriculumForm');
    const generateBtn = document.getElementById('generateBtn');
    const resultsSection = document.getElementById('resultsSection');
    const curriculumContent = document.getElementById('curriculumContent');
    const downloadBtn = document.getElementById('downloadBtn');

    let currentData = null;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        generateBtn.disabled = true;
        generateBtn.innerHTML = '<span class="loading-spinner"></span> Generating...';
        resultsSection.classList.add('hidden');
        curriculumContent.innerHTML = '';

        const skill = document.getElementById('skill').value;
        const level = document.getElementById('level').value;
        const industry = document.getElementById('industry').value;
        const semesters = document.getElementById('semesters').value;
        const hours = document.getElementById('hours').value;

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    skill: skill,
                    education_level: level,
                    semesters: semesters,
                    weekly_hours: hours,
                    industry_focus: industry
                })
            });

            if (!response.ok) throw new Error('Generation failed');

            const data = await response.json();
            currentData = data;

            renderCurriculum(data);
            resultsSection.classList.remove('hidden');

            setTimeout(() => {
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 100);

        } catch (error) {
            showAlert('Error creating curriculum: ' + error.message, 'error');
        } finally {
            generateBtn.disabled = false;
            generateBtn.innerHTML = '🚀 Generate My Curriculum';
        }
    });

    downloadBtn.addEventListener('click', async () => {
        if (!currentData) return;

        try {
            downloadBtn.disabled = true;
            downloadBtn.innerHTML = '<span class="loading-spinner"></span> Preparing PDF...';

            const response = await fetch('/api/download-pdf', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(currentData)
            });

            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;

            const skillName = document.getElementById('skill').value.replace(/[^a-z0-9]/gi, '_');
            a.download = `CurricuForge_${skillName}_Curriculum.pdf`;

            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            showAlert('PDF downloaded successfully!', 'success');

        } catch (error) {
            showAlert('Error downloading PDF: ' + error.message, 'error');
        } finally {
            downloadBtn.disabled = false;
            downloadBtn.innerHTML = '📥 Download PDF';
        }
    });

    function renderCurriculum(data) {
        let html = `
            <div style="margin-bottom: 2rem;">
                <h2 style="color:#2c3e50;">${data.program || 'Generated Curriculum'}</h2>
                <p style="color:#7f8c8d;">
                    ${data.semesters ? data.semesters.length : 0} Semesters • AI Generated
                </p>
            </div>
        `;

        if (data.semesters && Array.isArray(data.semesters)) {
            data.semesters.forEach((sem, index) => {
                html += `
                    <div class="semester-block" style="animation-delay:${index * 0.1}s;">
                        <h3>Semester ${sem.semester}</h3>
                        ${renderCourses(sem.courses)}
                    </div>
                `;
            });
        }

        curriculumContent.innerHTML = html;
    }

    function renderCourses(courses) {
        if (!courses || !Array.isArray(courses)) return '<p>No courses available.</p>';

        return courses.map((course, index) => `
            <div class="course-item" style="animation-delay:${index * 0.05}s;">
                <h4>${course.course_name}</h4>
                <ul>
                    ${(course.topics || []).map(t => `<li>${t}</li>`).join('')}
                </ul>
            </div>
        `).join('');
    }

    function showAlert(message, type = 'error') {
        const existing = document.querySelector('.alert');
        if (existing) existing.remove();

        const alert = document.createElement('div');
        alert.className = `alert alert-${type}`;
        alert.textContent = message;

        const inputSection = document.querySelector('.input-section');
        inputSection.parentNode.insertBefore(alert, inputSection);

        setTimeout(() => {
            alert.remove();
        }, 5000);
    }

    const inputs = document.querySelectorAll('input[required]');
    inputs.forEach(input => {
        input.addEventListener('invalid', e => {
            e.preventDefault();
            input.style.borderColor = '#e74c3c';
        });

        input.addEventListener('input', () => {
            input.style.borderColor = '#e1e8ed';
        });
    });
});


