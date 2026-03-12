# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    # Module 4 (Public)
    path("track/", views.track_case, name="track_case"),
    path("track/<str:tracking_id>/", views.track_case_detail, name="track_case_detail"),
    path("support/", views.support, name="support"),
    path("support/faq/", views.faq, name="faq"),
    path("support/feedback/", views.submit_feedback, name="submit_feedback"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("submissions/", views.submissions, name="submissions"),
    # Module 5 (Super Admin)
    path("analytics/", views.analytics_dashboard, name="analytics_dashboard"),
    path("reports/", views.reports, name="reports"),
    path("reports/export.csv", views.export_reports_csv, name="export_reports_csv"),
    path("users/", views.user_management, name="user_management"),
    path("users/new/", views.create_staff_account, name="create_staff_account"),
    path("users/<int:user_id>/edit/", views.edit_staff_account, name="edit_staff_account"),
    path("users/<int:user_id>/toggle-active/", views.toggle_staff_active, name="toggle_staff_active"),
    path("users/<int:user_id>/resend-activation/", views.resend_activation, name="resend_activation"),
    path("audit-logs/", views.audit_logs, name="audit_logs"),
    path("audit-logs/export.csv", views.export_audit_logs_csv, name="export_audit_logs_csv"),
    path("accounts/set-password/", views.set_password_view, name="set_password"),
    path("profile/", views.profile, name="profile"),
    path("submit/", views.submit_case, name="submit_case"),
    path("drafts/", views.drafts, name="drafts"),
    path("draft/<uuid:draft_id>/step/<int:step>/", views.draft_wizard, name="draft_wizard"),
    path("draft/<uuid:draft_id>/delete/", views.delete_draft, name="delete_draft"),
    path("case/<str:tracking_id>/step/<int:step>/", views.case_wizard, name="case_wizard"),
    path("case/<str:tracking_id>/edit/", views.edit_case, name="edit_case"),
    path("case/<str:tracking_id>/", views.case_detail, name="case_detail"),
    path("case/<str:tracking_id>/remarks/", views.add_case_remark, name="add_case_remark"),
    path("case/<str:tracking_id>/receive/", views.receive_case, name="receive_case"),
    path("case/<str:tracking_id>/return/", views.return_case, name="return_case"),
    path("case/<str:tracking_id>/assign/", views.assign_case, name="assign_case"),
    path("case/<str:tracking_id>/submit-for-approval/", views.submit_for_approval, name="submit_for_approval"),
    path("case/<str:tracking_id>/approve/", views.approve_case, name="approve_case"),
    path("case/<str:tracking_id>/return-for-correction/", views.return_for_correction, name="return_for_correction"),
    path("case/<str:tracking_id>/return-to-receiving/", views.return_to_receiving, name="return_to_receiving"),
    path("case/<str:tracking_id>/mark-numbered/", views.mark_numbered, name="mark_numbered"),
    path("case/<str:tracking_id>/release/", views.release_case, name="release_case"),

    # Protected media downloads
    path("documents/<int:doc_id>/download/", views.download_case_document, name="download_case_document"),
]
