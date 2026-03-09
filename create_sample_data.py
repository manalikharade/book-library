"""Script to populate the database with sample data"""
from datetime import datetime, timedelta, timezone
from app.database import SessionLocal, engine
from app.models import Book, Member, Borrowing, Base

def create_sample_data():
    """Create sample books, members, and borrowing records"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_books = db.query(Book).count()
        if existing_books > 0:
            print("Sample data already exists in the database")
            return
        
        # Sample Indian books
        books = [
            Book(
                title="The Great Indian Novel",
                author="Shashi Tharoor",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="Midnight's Children",
                author="Salman Rushdie",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="The God of Small Things",
                author="Arundhati Roy",
                available=False,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="The White Tiger",
                author="Aravind Adiga",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="Sacred Games",
                author="Vikram Chandra",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="The Namesake",
                author="Jhumpa Lahiri",
                available=False,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="Malgudi Days",
                author="R.K. Narayan",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="The Palace of Illusions",
                author="Chitra Banerjee Divakaruni",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="A Suitable Boy",
                author="Vikram Seth",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="The Inheritance of Loss",
                author="Kiran Desai",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
            Book(
                title="English, August",
                author="Upamanyu Chatterjee",
                available=True,
                created_at=datetime.now(tz=timezone.utc)
            ),
        ]
        
        db.add_all(books)
        db.commit()
        
        # Sample Indian members (Pune/Maharashtra focused)
        members = [
            Member(
                name="Manali Kharade",
                contact_no="+91-98765-43210",
                address="Flat 101, A Wing, Shree Ganesh Society, Baner, Pune, Maharashtra 411045",
                created_at=datetime.now(tz=timezone.utc)
            ),
            Member(
                name="Rahul Patil",
                contact_no="+91-98765-43211",
                address="203, Sai Heights, Pashan Road, Pune, Maharashtra 411021",
                created_at=datetime.now(tz=timezone.utc)
            ),
            Member(
                name="Priya Sharma",
                contact_no="+91-98765-43212",
                address="B-15, Green Valley Apartments, Kothrud, Pune, Maharashtra 411038",
                created_at=datetime.now(tz=timezone.utc)
            ),
            Member(
                name="Amit Deshpande",
                contact_no="+91-98765-43213",
                address="Flat 5B, Tower 2, Eon Free Zone, Kharadi, Pune, Maharashtra 411014",
                created_at=datetime.now(tz=timezone.utc)
            ),
            Member(
                name="Sneha Joshi",
                contact_no="+91-98765-43214",
                address="Ground Floor, Laxmi Nivas, JM Road, Pune, Maharashtra 411005",
                created_at=datetime.now(tz=timezone.utc)
            ),
            Member(
                name="Vikram Singh",
                contact_no="+91-98765-43215",
                address="Apartment 402, Skyline Residency, Viman Nagar, Pune, Maharashtra 411014",
                created_at=datetime.now(tz=timezone.utc)
            ),
            Member(
                name="Neha Pawar",
                contact_no="+91-98765-43216",
                address="Shop No. 12, Shivaji Housing Society, Bibwewadi, Pune, Maharashtra 411037",
                created_at=datetime.now(tz=timezone.utc)
            ),
        ]
        
        db.add_all(members)
        db.commit()
        
        # Sample borrowing records covering different scenarios
        now = datetime.now(tz=timezone.utc)
        borrowings = [
            # SCENARIO 1: Returned on time (no fine)
            Borrowing(
                book_id=1,  # The Great Indian Novel
                member_id=2,  # Rahul Patil
                borrowed_date=now - timedelta(days=15),
                due_date=now - timedelta(days=15) + timedelta(days=14),  # 14 days from borrow
                returned_date=now - timedelta(days=8),  # Returned 6 days early
                is_active=False,
                fine=0.0  # No late charge
            ),
            
            # SCENARIO 2: Returned 1 day late (fine = 10.0)
            Borrowing(
                book_id=2,  # Midnight's Children
                member_id=3,  # Priya Sharma
                borrowed_date=now - timedelta(days=16),
                due_date=now - timedelta(days=16) + timedelta(days=14),  # 14 days from borrow
                returned_date=now - timedelta(days=7),  # Returned 1 day late
                is_active=False,
                fine=10.0  # 1 day * 10.0 per day
            ),
            
            # SCENARIO 3: Returned 5 days late (fine = 50.0)
            Borrowing(
                book_id=4,  # The White Tiger
                member_id=4,  # Amit Deshpande
                borrowed_date=now - timedelta(days=20),
                due_date=now - timedelta(days=20) + timedelta(days=14),  # 14 days from borrow
                returned_date=now - timedelta(days=9),  # Returned 5 days late
                is_active=False,
                fine=50.0  # 5 days * 10.0 per day
            ),
            
            # SCENARIO 4: Returned 15 days late (fine = 150.0)
            Borrowing(
                book_id=5,  # Sacred Games
                member_id=5,  # Neha Pawar
                borrowed_date=now - timedelta(days=30),
                due_date=now - timedelta(days=30) + timedelta(days=14),  # 14 days from borrow
                returned_date=now - timedelta(days=15),  # Returned 15 days late
                is_active=False,
                fine=150.0  # 15 days * 10.0 per day
            ),
            
            # SCENARIO 5: Returned 30 days late (fine = 300.0)
            Borrowing(
                book_id=7,  # Malgudi Days
                member_id=6,  # Lisa Anderson
                borrowed_date=now - timedelta(days=45),
                due_date=now - timedelta(days=45) + timedelta(days=14),  # 14 days from borrow
                returned_date=now - timedelta(days=15),  # Returned 30 days late
                is_active=False,
                fine=300.0  # 30 days * 10.0 per day
            ),
            
            # SCENARIO 6: Returned 60 days late (would be 600.0 fine, but capped at max_fine of 500.0)
            Borrowing(
                book_id=8,  # The Palace of Illusions
                member_id=7,  # Vikram Singh
                borrowed_date=now - timedelta(days=75),
                due_date=now - timedelta(days=75) + timedelta(days=14),  # 14 days from borrow
                returned_date=now - timedelta(days=15),  # Returned 60 days late
                is_active=False,
                fine=500.0  # Capped at max_fine (would be 600.0 without cap)
            ),
            
            # SCENARIO 7: Currently borrowed, overdue by 6 days (no fine yet, fine will be calculated on return)
            Borrowing(
                book_id=3,  # The God of Small Things
                member_id=1,  # Manali Kharade
                borrowed_date=now - timedelta(days=20),
                due_date=now - timedelta(days=6),  # Due 6 days ago, now overdue
                returned_date=None,
                is_active=True,
                fine=0.0  # Will be calculated on return
            ),
            
            # SCENARIO 8: Currently borrowed, overdue by 50+ days (if returned now, would be capped at max_fine)
            Borrowing(
                book_id=6,  # The Namesake
                member_id=2,  # Rahul Patil
                borrowed_date=now - timedelta(days=65),
                due_date=now - timedelta(days=51),  # Due 51 days ago
                returned_date=None,
                is_active=True,
                fine=0.0  # Will be capped at max_fine on return
            ),
            
            # SCENARIO 9: Recently borrowed, still within due date
            Borrowing(
                book_id=9,  # A Suitable Boy
                member_id=3,  # Priya Sharma
                borrowed_date=now - timedelta(days=5),
                due_date=now + timedelta(days=9),  # Still 9 days until due
                returned_date=None,
                is_active=True,
                fine=0.0
            ),
            
            # SCENARIO 10: Recently borrowed, due soon
            Borrowing(
                book_id=10,  # The Inheritance of Loss
                member_id=4,  # Amit Deshpande
                borrowed_date=now - timedelta(days=13),
                due_date=now + timedelta(days=1),  # Due in 1 day
                returned_date=None,
                is_active=True,
                fine=0.0
            ),
        ]
        
        db.add_all(borrowings)
        db.commit()
        
        
        print("✓ Sample data created successfully!")
        print(f"  - {len(books)} books")
        print(f"  - {len(members)} members")
        print(f"  - {len(borrowings)} borrowing records")
        print("\nBorrowing Scenarios Covered:")
        print("  ✓ Returned on time (no fine)")
        print("  ✓ Returned 1 day late (fine = 10.0)")
        print("  ✓ Returned 5 days late (fine = 50.0)")
        print("  ✓ Returned 15 days late (fine = 150.0)")
        print("  ✓ Returned 30 days late (fine = 300.0)")
        print("  ✓ Returned 60 days late (fine capped at max_fine = 500.0)")
        print("  ✓ Currently overdue by 6 days (not yet returned)")
        print("  ✓ Currently overdue by 50+ days (would reach max_fine on return)")
        print("  ✓ Recently borrowed, within due date")
        print("  ✓ Recently borrowed, due soon")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
