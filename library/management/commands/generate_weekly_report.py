from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import BorrowRecord
import csv, os
from django.conf import settings
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate weekly report of borrows/returns for last 7 days.'

    def handle(self, *args, **options):
        today = timezone.now()
        start = today - timedelta(days=7)
        qs = BorrowRecord.objects.filter(requested_at__gte=start, requested_at__lte=today).select_related('user', 'book')
        outdir = os.path.join(settings.BASE_DIR, 'library_reports')
        os.makedirs(outdir, exist_ok=True)
        fname = os.path.join(outdir, f'weekly_report_{start.date()}_to_{today.date()}.csv')
        with open(fname, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user', 'user_role', 'book_title', 'status', 'requested_at', 'approved_at', 'due_date', 'returned_at'])
            for r in qs:
                writer.writerow([
                    r.user.get_full_name() or r.user.username,
                    getattr(r.user, 'role', ''),
                    r.book.title,
                    r.status,
                    r.requested_at.isoformat() if r.requested_at else '',
                    r.approved_at.isoformat() if r.approved_at else '',
                    r.due_date.isoformat() if r.due_date else '',
                    r.returned_at.isoformat() if r.returned_at else '',
                ])
        self.stdout.write(self.style.SUCCESS(f'Weekly report written to {fname}'))
