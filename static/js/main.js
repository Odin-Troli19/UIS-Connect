// Main JavaScript for UIS-Connect

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss flash messages after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add active class to links based on current URL
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Handle like button animations
    const likeButtons = document.querySelectorAll('.btn-like');
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            button.classList.add('active');
            // Remove the class after the animation completes
            setTimeout(() => {
                button.classList.remove('active');
            }, 300);
        });
    });

    // Character counter for post and comment textareas
    const textareas = document.querySelectorAll('textarea[data-max-length]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('data-max-length');
        const counterEl = document.createElement('small');
        counterEl.classList.add('text-muted', 'char-counter');
        counterEl.textContent = `0/${maxLength} characters`;
        
        textarea.parentNode.appendChild(counterEl);
        
        textarea.addEventListener('input', function() {
            const currentLength = textarea.value.length;
            counterEl.textContent = `${currentLength}/${maxLength} characters`;
            
            if (currentLength > maxLength) {
                counterEl.classList.add('text-danger');
            } else {
                counterEl.classList.remove('text-danger');
            }
        });
    });

    // Course filter functionality
    const courseFilterInput = document.getElementById('course-filter');
    if (courseFilterInput) {
        courseFilterInput.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const courseItems = document.querySelectorAll('.course-item');
            
            courseItems.forEach(item => {
                const courseText = item.textContent.toLowerCase();
                if (courseText.includes(filterValue)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // Confirm before unenrolling from a course
    const unenrollForms = document.querySelectorAll('.unenroll-form');
    unenrollForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to unenroll from this course?')) {
                e.preventDefault();
            }
        });
    });

    // Textarea auto-resize
    const autoResizeTextareas = document.querySelectorAll('textarea.auto-resize');
    autoResizeTextareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        // Trigger once on page load for textareas with content
        if (textarea.value.trim() !== '') {
            textarea.style.height = 'auto';
            textarea.style.height = (textarea.scrollHeight) + 'px';
        }
    });

    // Post preview functionality
    const previewButtons = document.querySelectorAll('.preview-button');
    previewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const postForm = this.closest('form');
            const contentTextarea = postForm.querySelector('textarea[name="content"]');
            const previewContainer = document.getElementById('post-preview');
            
            if (contentTextarea && previewContainer) {
                const content = contentTextarea.value;
                if (content.trim() === '') {
                    previewContainer.innerHTML = '<div class="alert alert-info">Nothing to preview. Please enter some content.</div>';
                } else {
                    // Convert newlines to <br> for display
                    const formattedContent = content.replace(/\n/g, '<br>');
                    previewContainer.innerHTML = `
                        <div class="card mb-3">
                            <div class="card-header bg-light">
                                <strong>Post Preview</strong>
                            </div>
                            <div class="card-body">
                                <p>${formattedContent}</p>
                            </div>
                        </div>
                    `;
                }
                
                // Scroll to preview
                previewContainer.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Handle course tags input
    const courseTagsInput = document.getElementById('course-tags-input');
    const selectedTagsContainer = document.getElementById('selected-tags');
    const hiddenTagsInput = document.getElementById('course_ids');
    
    if (courseTagsInput && selectedTagsContainer && hiddenTagsInput) {
        // Function to update the hidden input value
        function updateHiddenInput() {
            const tagElements = selectedTagsContainer.querySelectorAll('.course-tag');
            const tagIds = Array.from(tagElements).map(tag => tag.dataset.courseId);
            hiddenTagsInput.value = tagIds.join(',');
        }
        
        // Function to add a tag
        function addTag(courseId, courseCode) {
            // Check if tag already exists
            if (selectedTagsContainer.querySelector(`.course-tag[data-course-id="${courseId}"]`)) {
                return;
            }
            
            const tagElement = document.createElement('span');
            tagElement.classList.add('course-tag', 'me-2', 'mb-2', 'badge', 'bg-primary');
            tagElement.dataset.courseId = courseId;
            tagElement.innerHTML = `${courseCode} <button type="button" class="btn-close btn-close-white ms-1" aria-label="Remove"></button>`;
            
            // Add remove event listener
            const closeButton = tagElement.querySelector('.btn-close');
            closeButton.addEventListener('click', function() {
                tagElement.remove();
                updateHiddenInput();
            });
            
            selectedTagsContainer.appendChild(tagElement);
            updateHiddenInput();
        }
        
        // Handle course selection from dropdown
        const courseOptions = document.querySelectorAll('.course-option');
        courseOptions.forEach(option => {
            option.addEventListener('click', function() {
                const courseId = this.dataset.courseId;
                const courseCode = this.textContent.trim();
                addTag(courseId, courseCode);
                courseTagsInput.value = '';
            });
        });
    }

    // Notification system
    const notificationBell = document.getElementById('notification-bell');
    const notificationDropdown = document.getElementById('notification-dropdown');
    
    if (notificationBell && notificationDropdown) {
        // Function to fetch notifications (would connect to backend in production)
        function fetchNotifications() {
            // Simulated backend response
            return new Promise((resolve) => {
                setTimeout(() => {
                    resolve([
                        { id: 1, type: 'friend_request', from: 'jane_smith', time: '5 minutes ago' },
                        { id: 2, type: 'post_like', from: 'mike_johnson', postId: 123, time: '10 minutes ago' },
                        { id: 3, type: 'comment', from: 'david_brown', postId: 123, time: '30 minutes ago' }
                    ]);
                }, 300);
            });
        }
        
        // Function to render notifications
        async function updateNotifications() {
            const notifications = await fetchNotifications();
            const notificationContainer = notificationDropdown.querySelector('.dropdown-menu');
            
            // Update badge count
            const unreadCount = notifications.length;
            const badge = notificationBell.querySelector('.badge');
            
            if (unreadCount > 0) {
                if (badge) {
                    badge.textContent = unreadCount;
                } else {
                    const newBadge = document.createElement('span');
                    newBadge.className = 'position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger';
                    newBadge.textContent = unreadCount;
                    notificationBell.appendChild(newBadge);
                }
            } else if (badge) {
                badge.remove();
            }
            
            // Update dropdown content
            notificationContainer.innerHTML = '';
            
            if (notifications.length === 0) {
                notificationContainer.innerHTML = '<div class="dropdown-item text-center text-muted">No new notifications</div>';
                return;
            }
            
            notifications.forEach(notification => {
                const item = document.createElement('a');
                item.className = 'dropdown-item';
                
                let content = '';
                if (notification.type === 'friend_request') {
                    content = `<strong>${notification.from}</strong> sent you a friend request`;
                    item.href = `/friends`;
                } else if (notification.type === 'post_like') {
                    content = `<strong>${notification.from}</strong> liked your post`;
                    item.href = `/posts/${notification.postId}`;
                } else if (notification.type === 'comment') {
                    content = `<strong>${notification.from}</strong> commented on your post`;
                    item.href = `/posts/${notification.postId}`;
                }
                
                item.innerHTML = `
                    <div>${content}</div>
                    <small class="text-muted">${notification.time}</small>
                `;
                
                notificationContainer.appendChild(item);
            });
            
            // Add "Mark all as read" button
            const markAllBtn = document.createElement('button');
            markAllBtn.className = 'dropdown-item text-primary text-center';
            markAllBtn.textContent = 'Mark all as read';
            markAllBtn.addEventListener('click', function(e) {
                e.preventDefault();
                // Would connect to backend to mark notifications as read
                const badge = notificationBell.querySelector('.badge');
                if (badge) badge.remove();
            });
            
            const divider = document.createElement('div');
            divider.className = 'dropdown-divider';
            
            notificationContainer.appendChild(divider);
            notificationContainer.appendChild(markAllBtn);
        }
        
        // Check for notifications on page load and when clicking the bell
        updateNotifications();
        notificationBell.addEventListener('click', updateNotifications);
    }

    // On scroll load more posts for infinite scrolling
    const postFeed = document.querySelector('.post-feed');
    let isLoading = false;
    let page = 1;
    
    if (postFeed) {
        window.addEventListener('scroll', function() {
            // Check if we're near the bottom of the page
            if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
                if (!isLoading) {
                    loadMorePosts();
                }
            }
        });
        
        async function loadMorePosts() {
            isLoading = true;
            const loadingIndicator = document.createElement('div');
            loadingIndicator.className = 'text-center py-3';
            loadingIndicator.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
            postFeed.appendChild(loadingIndicator);
            
            // In a real app, this would fetch from the server
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Remove loading indicator
            loadingIndicator.remove();
            isLoading = false;
            page++;
        }
    }
});