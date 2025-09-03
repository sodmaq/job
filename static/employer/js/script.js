function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  const content = document.querySelector('.content');
  sidebar.classList.toggle('active');
  content.classList.toggle('active');
}

// JavaScript to handle edit and delete modal actions
document.addEventListener("DOMContentLoaded", function() {
    // Edit Job Modal
    var editJobModal = document.getElementById('editJobModal');
    editJobModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var jobId = button.getAttribute('data-job-id');
        var jobTitle = button.getAttribute('data-job-title');
        var department = button.getAttribute('data-department');
        var location = button.getAttribute('data-location');
        var experience = button.getAttribute('data-experience');

        // Fill the modal with job details
        document.getElementById('editJobTitle').value = jobTitle;
        document.getElementById('editDepartment').value = department;
        document.getElementById('editLocation').value = location;
        document.getElementById('editExperienceLevel').value = experience;
    });

    // Delete Job Modal
    var deleteJobModal = document.getElementById('deleteJobModal');
    deleteJobModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget;
        var jobId = button.getAttribute('data-job-id');
        document.getElementById('confirmDeleteBtn').onclick = function() {
            // Call API to delete job with jobId
            console.log("Deleting job ID:", jobId);
            // Close modal after deletion
            var modal = bootstrap.Modal.getInstance(deleteJobModal);
            modal.hide();
        };
    });
});



// JavaScript to handle modals for applicants
document.addEventListener("DOMContentLoaded", function() {
    // View Applicant Details Modal
    var applicantDetailsModal = document.getElementById('applicantDetailsModal');
    applicantDetailsModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var applicantId = button.getAttribute('data-applicant-id');
        var applicantName = button.getAttribute('data-applicant-name');
        var jobTitle = button.getAttribute('data-job-title');

        // Populate modal with applicant details
        document.getElementById('applicantName').textContent = applicantName;
        document.getElementById('jobTitle').textContent = jobTitle;
        document.getElementById('resumeLink').setAttribute('href', 'resume/' + applicantId + '.pdf'); // Dynamically link resume
    });

    // Interview Invitation Modal
    var interviewModal = document.getElementById('interviewModal');
    interviewModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var applicantId = button.getAttribute('data-applicant-id');
        var applicantName = button.getAttribute('data-applicant-name');
        var jobTitle = button.getAttribute('data-job-title');

        // Populate modal with applicant name and job title
        document.getElementById('interviewApplicantName').textContent = applicantName;
        document.getElementById('interviewJobTitle').textContent = jobTitle;
    });

    // Reject Applicant Modal
    var rejectModal = document.getElementById('rejectModal');
    rejectModal.addEventListener('show.bs.modal', function(event) {
        var button = event.relatedTarget; // Button that triggered the modal
        var applicantId = button.getAttribute('data-applicant-id');
        var applicantName = button.getAttribute('data-applicant-name');
        var jobTitle = button.getAttribute('data-job-title');

        // Populate modal with applicant name and job title
        document.getElementById('rejectApplicantName').textContent = applicantName;
        document.getElementById('rejectJobTitle').textContent = jobTitle;
    });
});


// JavaScript to handle modals for rescheduling, canceling, accepting, and rejecting interviews
document.addEventListener("DOMContentLoaded", function() {
    // Accept Candidate Modal
    var acceptModal = document.getElementById('acceptModal');
    acceptModal.addEventListener('show.bs.modal', function(event) {
        // Populate modal with candidate details
        console.log("Accept candidate modal opened.");
    });

    // Reject Candidate Modal
    var rejectModal = document.getElementById('rejectModal');
    rejectModal.addEventListener('show.bs.modal', function(event) {
        // Populate modal with candidate details
        console.log("Reject candidate modal opened.");
    });

    // Reschedule Button click handler
    document.getElementById('rescheduleBtn').addEventListener('click', function() {
        var newDate = document.getElementById('newInterviewDate').value;
        var newTime = document.getElementById('newInterviewTime').value;
        if (newDate && newTime) {
            alert('Interview successfully rescheduled to ' + newDate + ' at ' + newTime);
            var modal = bootstrap.Modal.getInstance(acceptModal);
            modal.hide();
        } else {
            alert('Please select both date and time for the interview.');
        }
    });

    // Cancel Interview Button click handler
    document.getElementById('cancelInterviewBtn').addEventListener('click', function() {
        alert('Interview has been canceled.');
        var modal = bootstrap.Modal.getInstance(rejectModal);
        modal.hide();
    });

    // Accept Button click handler
    document.getElementById('acceptCandidateBtn').addEventListener('click', function() {
        alert('Candidate has been accepted!');
        var modal = bootstrap.Modal.getInstance(acceptModal);
        modal.hide();
    });

    // Reject Button click handler
    document.getElementById('rejectCandidateBtn').addEventListener('click', function() {
        alert('Candidate has been rejected.');
        var modal = bootstrap.Modal.getInstance(rejectModal);
        modal.hide();
    });
});
