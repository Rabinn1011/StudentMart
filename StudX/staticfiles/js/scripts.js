var swiper = new Swiper(".mySwiper", {
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
        delay: 4000,
        disableOnInteraction: false,
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
});

//dropdown menu on clivk action

const profileIcon = document.getElementById('profile-icon');
const dropdownMenu = document.getElementById('dropdown-menu');

// Toggle the dropdown menu on click
profileIcon.addEventListener('click', (e) => {
    e.preventDefault(); // Prevent default anchor behavior
    e.stopPropagation(); // Prevent event from bubbling up
    dropdownMenu.style.display =
        dropdownMenu.style.display === 'block' ? 'none' : 'block';
});

// Hide the dropdown menu when clicking outside
document.addEventListener('click', () => {
    dropdownMenu.style.display = 'none';
});

//delete product (profile ko seller_profile.html ma xa,,, yeta milena! idk why) functionality ko

document.querySelectorAll('.red-button').forEach(button => {
    button.addEventListener('click', function (event) {
        const action = button.getAttribute('data-action');

        if (action === 'delete-product') {

            event.preventDefault();
            const confirmBox = document.getElementById('custom-confirm');
            confirmBox.style.display = 'flex';

            // Handle Yes button
            document.getElementById('confirm-yes').onclick = function () {
                window.location.href = button.href; // Proceed with deletion
            };

            // Handle No button
            document.getElementById('confirm-no').onclick = function () {
                confirmBox.style.display = 'none';
            };
        }

    });
});


// js for taking comment and replies
$(document).ready(function () {
    // Format date like "April 16, 2025"
    function formatDate(dateString) {
        let date = new Date(dateString);
        let options = { year: "numeric", month: "long", day: "numeric" };
        return date.toLocaleDateString("en-US", options);
    }

    // Submit comment
    $("#comment-form").submit(function (e) {
        e.preventDefault();
        const formData = $(this).serialize();

        $.ajax({
            type: "POST",
            url: "/add_comment/",
            data: formData,
            success: function (response) {
                if (response.error) {
                    alert(response.error);
                } else {
                    const formattedDate = formatDate(response.created_at);
                    const deleteButton = `<button class="delete-btn" data-id="${response.id}">Delete Comment</button>`;
                    const replyButtonHTML = isSeller ? `<button class="reply-btn" data-id="${response.id}">Reply</button>` : "";

                    const newCommentHTML = `
                        <li id="comment-${response.id}" class="comment">
                            <div class="comment-header">
                                <strong>${response.user}</strong>
                                <span class="comment-date">${formattedDate}</span>
                                ${deleteButton}
                            </div>
                            <div class="comment-content">
                                ${response.content}
                            </div>
                            ${replyButtonHTML}
                            <div id="reply-${response.id}" class="reply-textarea" style="display:none;">
                                <textarea class="reply-content" placeholder="Write a reply..."></textarea>
                                <button class="reply-submit" data-parent="${response.id}">Post Reply</button>
                            </div>
                            <ul class="reply-list"></ul>
                        </li>
                    `;

                    if (response.parent) {
                        $(`#comment-${response.parent} .reply-list`).append(newCommentHTML);
                    } else {
                        $("#comment-list").prepend(newCommentHTML);
                    }

                    // Render replies if included
                    if (response.replies) {
                        response.replies.forEach(function (reply) {
                            const formattedReplyDate = formatDate(reply.created_at);
                            const replyHTML = `
                                <li class="reply">
                                    <div class="comment-header">
                                        <strong>${reply.user}</strong>
                                        <span class="comment-date">${formattedReplyDate}</span>
                                    </div>
                                    <div class="comment-content">
                                        ${reply.content}
                                    </div>
                                </li>
                            `;
                            $(`#comment-${response.id} .reply-list`).append(replyHTML);
                        });
                    }

                    applyCommentStyles();
                    bindDeleteEvent();
                    $("#comment-content").val("");
                    $("#parent-id").val("");
                }
            }
        });
    });

    // Toggle reply textarea
    $(document).on("click", ".reply-btn", function () {
        const parentID = $(this).data("id");
        const replyTextarea = $("#reply-" + parentID);
        replyTextarea.toggle();
        $(this).text(replyTextarea.is(":visible") ? "Cancel Reply" : "Reply");
    });

    // Post reply
    $(document).on("click", ".reply-submit", function () {
        const parentID = $(this).data("parent");
        const replyContent = $("#reply-" + parentID + " .reply-content").val();
        const productID = $("input[name='product_id']").val();

        if (replyContent.trim() === "") {
            alert("Reply content cannot be empty!");
            return;
        }

        $.ajax({
            type: "POST",
            url: "/add_comment/",
            data: {
                product_id: productID,
                parent: parentID,
                content: replyContent,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
            },
            success: function (response) {
                if (response.error) {
                    alert(response.error);
                } else {
                    const formattedDate = formatDate(response.created_at);
                    const deleteButton = `<button class="delete-btn" data-id="${response.id}">Delete Reply</button>`;
                    var displayName = response.reply_display_name || response.user;
                    const newReplyHTML = `
                        <li class="reply" id="reply-${response.id}">
                            <div class="comment-header">
                                <strong>${displayName}<i class="fas fa-circle-check verified-icon"></i></strong>
                                <span class="comment-date">${formattedDate}</span>
                                ${deleteButton}
                            </div>
                            <div class="comment-content">
                                ${response.content}
                            </div>
                        </li>
                    `;

                    $("#comment-" + parentID + " .reply-list").append(newReplyHTML);
                    applyCommentStyles();
                    bindDeleteEvent();

                    $("#reply-" + parentID).hide();
                    $("#reply-" + parentID + " .reply-content").val("");
                    $(".reply-btn[data-id='" + parentID + "']").text("Reply");
                }
            }
        });
    });

    // Delete comment or reply
    function bindDeleteEvent() {
        $(document).off("click", ".delete-btn").on("click", ".delete-btn", function () {
            const commentID = $(this).data("id");

            if (!confirm("Are you sure you want to delete this comment?")) return;

            $.ajax({
                type: "POST",
                url: `/delete_comment/${commentID}/`,
                data: {
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
                },
                success: function (response) {
                    if (response.success) {
                        $(`#comment-${commentID}`).remove();
                    } else {
                        alert("Error deleting comment.");
                    }
                }
            });
        });
    }

    bindDeleteEvent();

    // Style buttons and headers
    function applyCommentStyles() {
            // Apply style to comment usernames
        $(".comment > .comment-header strong").css("color", "#007bff"); // Blue for main comments

            // Apply style to reply usernames
        $(".reply > .comment-header strong").css("color", "#28a745"); // Green for replies



        $(".reply-btn").css({
            background: "#28a745",
            color: "white",
            border: "none",
            padding: "5px 10px",
            cursor: "pointer"
        }).hover(function () {
            $(this).css("background", "#218838");
        }, function () {
            $(this).css("background", "#28a745");
        });

        $(".delete-btn").css({
            backgroundColor: "#e74c3c",
            color: "white",
            padding: "5px 10px",
            border: "none",
            borderRadius: "3px",
            cursor: "pointer",
            fontSize: "14px",
            marginLeft: "10px"
        }).hover(function () {
            $(this).css("background", "#c82333");
        }, function () {
            $(this).css("background", "#dc3545");
        });
    }
});




 //js for handling delete comment and replies

$(document).ready(function () {
        // Open the delete modal for comments and replies
        $(document).on('click', '.delete-comment, .delete-reply', function () {
            const type = $(this).data('type');  // comment or reply
            const id = $(this).data('id');      // comment or reply id
            const parentId = $(this).data('parent');  // Only for replies

            // Set the message in the modal based on the type (comment/reply)
            if (type === 'comment') {
                $('#delete-message').text('Are you sure you want to delete this comment?');
            } else {
                $('#delete-message').text('Are you sure you want to delete this reply?');
            }

            // Store the type and id in the modal for later use
            $('#deleteModal').data('type', type).data('id', id).data('parent-id', parentId);
            $('#deleteModal').show();
        });

        // Confirm deletion (send request to server)
        $('#confirmDelete').on('click', function () {
            const type = $('#deleteModal').data('type');
            const id = $('#deleteModal').data('id');
            const parentId = $('#deleteModal').data('parent-id');

            // Form the URL based on the type (comment/reply)
            const url = (type === 'comment') ? `/delete_comment/${id}/` : `/delete_reply/${id}/`;
            const data = {
                'csrfmiddlewaretoken': $("input[name='csrfmiddlewaretoken']").val()
            };

            $.ajax({
                url: url,
                type: 'POST',
                data: data,
                success: function (response) {
                    if (response.success) {
                        if (type === 'comment') {
                            $(`#comment-${id}`).remove();  // Remove the comment
                        } else {
                            $(`#reply-${id}`).remove();    // Remove the reply
                        }
                    } else {
                        alert('Failed to delete!');
                    }
                    $('#deleteModal').hide();
                },
                error: function () {
                    alert('Error occurred while deleting.');
                    $('#deleteModal').hide();
                }
            });
        });

        // Cancel deletion
        $('#cancelDelete').on('click', function () {
            $('#deleteModal').hide();
        });
    });

