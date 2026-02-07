from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io

def create_pdf(curriculum_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title Style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Content Styles
    h1_style = styles['Heading1']
    h2_style = styles['Heading2']
    normal_style = styles['Normal']

    # Program Title
    program_name = curriculum_data.get('program', 'Curriculum')
    story.append(Paragraph(program_name, title_style))
    story.append(Spacer(1, 12))

    # Semesters
    semesters = curriculum_data.get('semesters', [])
    for semester in semesters:
        sem_num = semester.get('semester', '?')
        story.append(Paragraph(f"Semester {sem_num}", h1_style))
        story.append(Spacer(1, 6))

        courses = semester.get('courses', [])
        for course in courses:
            course_name = course.get('course_name', 'Unknown Course')
            story.append(Paragraph(course_name, h2_style))
            
            topics = course.get('topics', [])
            topic_items = [ListItem(Paragraph(t, normal_style)) for t in topics]
            story.append(ListFlowable(topic_items, bulletType='bullet', start='circle'))
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer