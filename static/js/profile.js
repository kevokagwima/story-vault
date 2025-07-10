document.addEventListener("DOMContentLoaded", function () {
  // Tab switching functionality
  const tabs = document.querySelectorAll(".tab");
  const tabContents = document.querySelectorAll(".tab-content");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      // Remove active class from all tabs and contents
      tabs.forEach((t) => t.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      // Add active class to clicked tab and corresponding content
      tab.classList.add("active");
      const tabId = tab.getAttribute("data-tab");
      document.getElementById(tabId).classList.add("active");
    });
  });

  // Profile picture edit button
  const editPictureBtn = document.querySelector(".edit-picture-btn");
  if (editPictureBtn) {
    editPictureBtn.addEventListener("click", function (e) {
      e.preventDefault();
      // In a real app, this would open a file picker
      alert(
        "Feature coming soon! You will be able to upload a new profile picture."
      );
    });
  }

  // Post edit/delete buttons
  const editPostButtons = document.querySelectorAll(".edit-post");
  const deletePostButtons = document.querySelectorAll(".delete-post");

  editPostButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      const postCard = this.closest(".post-card");
      // In a real app, this would open an edit form
      alert("Edit post feature coming soon!");
    });
  });

  deletePostButtons.forEach((button) => {
    button.addEventListener("click", function (e) {
      e.preventDefault();
      if (confirm("Are you sure you want to delete this post?")) {
        const postCard = this.closest(".post-card");
        postCard.style.opacity = "0";
        setTimeout(() => {
          postCard.remove();
          // In a real app, you would also make an API call to delete from the server
        }, 300);
      }
    });
  });

  // Update form submission
  const updateForm = document.querySelector(".update-form");
  if (updateForm) {
    updateForm.addEventListener("submit", function (e) {
      e.preventDefault();
      // In a real app, this would send data to the server
      alert(
        "Profile updated successfully! (This is a demo - no changes were actually saved)"
      );
    });
  }
});
