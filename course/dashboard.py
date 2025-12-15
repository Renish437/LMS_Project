from unfold.widgets import ChartWidget
from django.db.models import Count
from .models import Course


class CourseStatusChart(ChartWidget):
    title = "Courses by Status"
    type = "bar"  # bar | line | pie | doughnut

    def get_data(self):
        print("Dashboard loaded")
        qs = (
            Course.objects
            .values("status")
            .annotate(total=Count("id"))
        )

        labels = [item["status"] or "Unknown" for item in qs]
        data = [item["total"] for item in qs]

        return {
            "labels": labels,
            "datasets": [
                {
                    "label": "Courses",
                    "data": data,
                }
            ],
        }
