from pathlib import Path
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from shop.models import Product


class Command(BaseCommand):
    help = 'Bulk upload local product images to Cloudinary and update Product image fields.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be uploaded without saving changes.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        SOURCE_IMAGE_FOLDER = settings.BASE_DIR / 'media' / 'products'
        if not SOURCE_IMAGE_FOLDER.exists():
            self.stdout.write(
                self.style.ERROR(f'Folder not found: {SOURCE_IMAGE_FOLDER}')
            )
            return

        image_files = {
            file.name.lower(): file
            for file in SOURCE_IMAGE_FOLDER.rglob('*')
            if file.is_file()
        }

        products = Product.objects.all()

        uploaded_count = 0
        missing_count = 0

        for product in products:
            if not product.image:
                self.stdout.write(
                    self.style.WARNING(f'{product.name}: no image field value')
                )
                continue

            filename = Path(product.image.name).name
            local_file = image_files.get(filename.lower())

            if not local_file:
                self.stdout.write(
                    self.style.WARNING(f'Missing image for {product.name}: {filename}')
                )
                missing_count += 1
                continue

            self.stdout.write(f'Found image for {product.name}: {local_file}')

            if not dry_run:
                with open(local_file, 'rb') as f:
                    product.image.save(filename, File(f), save=True)

                self.stdout.write(
                    self.style.SUCCESS(f'Uploaded: {product.name}')
                )

            uploaded_count += 1

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Dry run complete. {uploaded_count} images found, {missing_count} missing.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Upload complete. {uploaded_count} images uploaded, {missing_count} missing.'
                )
            )
