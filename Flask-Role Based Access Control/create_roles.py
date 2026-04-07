from app import Role, db, app

def create_roles():
    with app.app_context():
        admin = Role(id=1, name='Admin')
        teacher = Role(id=2, name='Teacher')
        staff = Role(id=3, name='Staff')
        student = Role(id=4, name='Student')

        db.session.add(admin)
        db.session.add(teacher)
        db.session.add(staff)
        db.session.add(student)

        db.session.commit()
        print("Roles created successfully!")

if __name__ == '__main__':
    create_roles()