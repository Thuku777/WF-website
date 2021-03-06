import csv
from django.core.management.base import BaseCommand, CommandError

from contact.models import (
    Meeting,
    MeetingIndexPage,
    Organization,
    OrganizationIndexPage,
    Person,
    PersonIndexPage
)


class Command(BaseCommand):
    help = "Import Authors from Drupal site"

    def add_arguments(self, parser):
        parser.add_argument("--file", action="store", type=str)

    def handle(self, *args, **options):
        with open(options["file"]) as import_file:
            # Get index pages for use when saving entities
            meeting_index_page = MeetingIndexPage.objects.get()
            organization_index_page = OrganizationIndexPage.objects.get()
            person_index_page = PersonIndexPage.objects.get()

            authors = csv.DictReader(import_file)

            for author in authors:
                # Check for entity type among:
                # - Meeting
                # - Organization
                # - Person
                # with the condition to check for corrections to person names
                author_is_meeting = author["meeting_name"] is not ""
                author_is_organization = author["organization_name"] is not ""
                author_is_person = (
                    author["family_name"] is not "" or
                    author["given_name"] is not "" or
                    author["corrected_family_name"] is not "" or
                    author["corrected_given_name"] is not ""
                )

                if author_is_meeting:
                    meeting = Meeting(
                        title=author["meeting_name"],
                        drupal_full_name=author["drupal_full_name"]
                    )

                    meeting_index_page.add_child(instance=meeting)

                    meeting_index_page.save()
                elif author_is_organization:
                    organization = Organization(
                        title=author["organization_name"],
                        drupal_full_name=author["drupal_full_name"]
                    )

                    organization_index_page.add_child(instance=organization)

                    organization_index_page.save()
                elif author_is_person:
                    author_name_corrected = (
                        author["corrected_family_name"] is not "" or
                        author["corrected_given_name"] is not ""
                    )

                    if author_name_corrected:
                        given_name = author["corrected_given_name"]
                        family_name = author["corrected_family_name"]
                    else:
                        given_name = author["given_name"]
                        family_name = author["family_name"]

                    person = Person(
                        given_name=given_name,
                        family_name=family_name,
                        drupal_full_name=author["drupal_full_name"]
                    )

                    person_index_page.add_child(instance=person)

                    person_index_page.save()
                else:
                    print("unknown")

        self.stdout.write("All done!")
