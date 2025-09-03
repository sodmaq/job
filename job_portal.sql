-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 03, 2025 at 08:32 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `job_portal`
--

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `job_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `resume_url` text DEFAULT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `applied_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`id`, `user_id`, `job_id`, `name`, `email`, `phone`, `resume_url`, `status`, `applied_at`) VALUES
(1, 1, 2, NULL, NULL, NULL, NULL, 'rejected', '2025-07-25 03:05:51'),
(2, 1, 3, NULL, NULL, NULL, NULL, 'rejected', '2025-07-25 03:05:55'),
(3, 1, 1, NULL, NULL, NULL, NULL, 'rejected', '2025-07-25 03:05:57'),
(4, 1, 7, NULL, NULL, NULL, NULL, 'rejected', '2025-07-28 03:24:02'),
(5, 1, 4, NULL, NULL, NULL, NULL, 'rejected', '2025-07-28 03:24:03'),
(6, 2, 4, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:15:58'),
(7, 2, 3, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:16:00'),
(8, 2, 2, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:16:03'),
(9, 2, 7, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:16:05'),
(10, 2, 11, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:16:06'),
(11, 2, 9, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:16:07'),
(12, 2, 1, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:16:10'),
(13, 1, 11, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:33:40'),
(14, 1, 9, NULL, NULL, NULL, NULL, 'rejected', '2025-08-05 09:33:43'),
(15, 3, 7, NULL, NULL, NULL, NULL, 'rejected', '2025-08-19 12:44:03'),
(16, 3, 9, NULL, NULL, NULL, NULL, 'rejected', '2025-08-19 12:45:58'),
(21, 4, 7, NULL, NULL, NULL, NULL, 'accepted', '2025-08-26 23:00:00'),
(28, 5, 7, NULL, NULL, NULL, NULL, 'accepted', '2025-08-29 01:22:42'),
(30, 6, 7, NULL, NULL, NULL, NULL, 'accepted', '2025-08-29 02:30:22'),
(31, 7, 4, NULL, NULL, NULL, NULL, 'rejected', '2025-09-01 16:07:21'),
(32, 7, 7, NULL, NULL, NULL, NULL, 'accepted', '2025-09-01 16:07:26');

-- --------------------------------------------------------

--
-- Table structure for table `employers`
--

CREATE TABLE `employers` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employers`
--

INSERT INTO `employers` (`id`, `name`, `email`, `password`, `created_at`) VALUES
(1, 'Tech World', 'tech@gmail.com', 'pass', '2025-07-25 02:37:22'),
(2, 'CodeCraft Inc.', 'codecraft@gmail.com', 'pass', '2025-07-25 03:19:22'),
(3, 'InnovaSoft Solutions', 'innova@soft.com', 'pass', '2025-07-25 03:45:00');

-- --------------------------------------------------------

--
-- Table structure for table `interviews`
--

CREATE TABLE `interviews` (
  `id` int(11) NOT NULL,
  `applicant_id` int(11) NOT NULL,
  `employer_id` int(11) NOT NULL,
  `job_id` int(11) DEFAULT NULL,
  `interview_date` datetime NOT NULL,
  `meeting_link` varchar(255) DEFAULT NULL,
  `status` enum('scheduled','completed','cancelled') DEFAULT 'scheduled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `interviews`
--

INSERT INTO `interviews` (`id`, `applicant_id`, `employer_id`, `job_id`, `interview_date`, `meeting_link`, `status`) VALUES
(7, 5, 2, 4, '2025-08-30 14:23:00', 'https://us05web.zoom.us/j/89864924230?pwd=uWbnGOYSXQxfWdAKRdWaVb0GZXPFF9.1', 'scheduled'),
(8, 5, 2, 7, '2025-08-30 14:27:00', 'https://us05web.zoom.us/j/89864924230?pwd=uWbnGOYSXQxfWdAKRdWaVb0GZXPFF9.1', 'scheduled'),
(9, 6, 2, 7, '2025-08-30 15:30:00', 'https://us05web.zoom.us/j/89864924230?pwd=uWbnGOYSXQxfWdAKRdWaVb0GZXPFF9.1', 'completed'),
(10, 7, 2, 7, '2025-09-03 10:00:00', 'https://us05web.zoom.us/j/89864924230?pwd=uWbnGOYSXQxfWdAKRdWaVb0GZXPFF9.1', 'completed'),
(11, 7, 2, 4, '2025-09-06 10:00:00', 'https://us05web.zoom.us/j/89864924230?pwd=uWbnGOYSXQxfWdAKRdWaVb0GZXPFF9.1', 'cancelled');

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` int(11) NOT NULL,
  `company` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `department` varchar(100) DEFAULT NULL,
  `job_type` varchar(50) DEFAULT NULL,
  `experience` varchar(100) DEFAULT NULL,
  `salary` varchar(50) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `skills` text DEFAULT NULL,
  `employer_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`id`, `company`, `title`, `department`, `job_type`, `experience`, `salary`, `location`, `description`, `skills`, `employer_id`, `created_at`) VALUES
(1, 'Tech World', 'Frontend Developer', 'Engineering', 'Full-Time', '2+ years', '₦250,000', 'Lagos, Nigeria', 'Tech World is seeking a creative and detail-oriented Frontend Developer to join our engineering team. The ideal candidate should have experience in building responsive, modern web interfaces using HTML, CSS, JavaScript, and frameworks like React or Vue. You’ll work closely with backend engineers and UI/UX designers to translate high-fidelity wireframes into pixel-perfect pages. A solid understanding of cross-browser compatibility and performance optimization is required.', 'HTML, CSS, JavaScript, React, Git', 1, '2025-07-25 03:05:10'),
(2, 'Tech World', 'Data Analyst Intern', 'Data & Analytics', 'Internship', '0–1 year', '₦100,000', 'Remote', 'We are looking for an enthusiastic Data Analyst Intern eager to work with large datasets to derive actionable insights. You will assist the analytics team with data cleaning, report generation, and visualization tasks. This role is perfect for students or recent graduates with strong Excel skills and familiarity with Python or SQL. The internship is remote with flexible hours and hands-on mentorship.', 'Excel, SQL, Python, Data Visualization', 1, '2025-07-25 03:07:23'),
(3, 'Tech World', 'Senior Backend Engineer', 'Software Engineering', 'Full-Time', '5+ years', '₦600,000', 'Abuja, Nigeria', 'Tech World is hiring a Senior Backend Engineer to lead the development of scalable backend services. You’ll architect and implement RESTful APIs, manage databases, and ensure high availability and performance of our systems. Experience with Python (Flask/Django), cloud deployment (AWS or GCP), CI/CD pipelines, and system security practices is essential. You’ll also mentor junior developers and contribute to architectural decisions.', 'Python, Django, PostgreSQL, REST API, AWS, Docker', 1, '2025-07-25 03:09:45'),
(4, 'CodeCraft Inc.', 'Software Engineer', 'Technology', 'Full-Time', '3+ years', '₦400,000', 'Lagos, Nigeria', 'CodeCraft Inc. is seeking a Software Engineer with solid experience in full-stack development using Python and JavaScript. You will work on scalable enterprise systems, participate in system design, and write high-performance code. Familiarity with cloud services like AWS and CI/CD practices is a plus.', 'Python, JavaScript, Flask, AWS, Git, MySQL', 2, '2025-07-25 03:50:10'),
(5, 'CodeCraft Inc.', 'UI/UX Designer', 'Design', 'Full-Time', '2+ years', '₦300,000', 'Remote', 'We are hiring a UI/UX Designer to craft engaging user experiences for our mobile and web apps. The ideal candidate has a strong eye for design, proficiency in tools like Figma or Adobe XD, and a solid understanding of user-centered design principles.', 'Figma, Adobe XD, User Research, Wireframing, Prototyping', 2, '2025-07-25 03:52:31'),
(6, 'CodeCraft Inc.', 'Technical Writer', 'Content', 'Part-Time', '1+ year', '₦200,000', 'Remote', 'Join our documentation team to write clear and concise technical documents, manuals, and release notes. You’ll work closely with engineers to understand complex systems and translate them into user-friendly documentation.', 'Technical Writing, Markdown, Git, API Docs, Communication', 2, '2025-07-25 03:54:42'),
(7, 'CodeCraft Inc.', 'QA Automation Engineer', 'Quality Assurance', 'Full-Time', '3+ years', '₦350,000', 'Abuja, Nigeria', 'We are looking for a detail-oriented QA Automation Engineer to build and maintain automated test suites for our core applications. You should have experience with Selenium or similar tools and a strong understanding of SDLC and Agile methodologies.', 'Selenium, Python, TestNG, Jenkins, Agile', 2, '2025-07-25 03:57:10'),
(8, 'CodeCraft Inc.', 'IT Support Specialist', 'IT & Infrastructure', 'Contract', '1–2 years', '₦180,000', 'Ibadan, Nigeria', 'Provide first-line technical support to our internal teams and help maintain infrastructure including systems, networks, and devices. Basic knowledge of hardware, troubleshooting, and remote support tools is essential.', 'Windows, Networking, Troubleshooting, IT Helpdesk, Communication', 2, '2025-07-25 03:59:00'),
(9, 'InnovaSoft Solutions', 'Frontend Developer', 'Development', 'Full-Time', '2+ years', '₦400,000', 'Lagos, Nigeria', 'Seeking a frontend developer skilled in modern frameworks like React or Vue.js to build engaging interfaces.', 'HTML, CSS, JavaScript, React, UI/UX', 3, '2025-07-28 04:03:23'),
(10, 'InnovaSoft Solutions', 'Backend Developer', 'Development', 'Full-Time', '3+ years', '₦500,000', 'Abuja, Nigeria', 'Join our backend team to design APIs, manage databases, and support scalable platforms.', 'Node.js, PHP, MySQL, REST API, Docker', 3, '2025-07-28 04:03:23'),
(11, 'InnovaSoft Solutions', 'Data Analyst', 'Analytics', 'Contract', '1+ year', '₦300,000', 'Remote', 'Analyze business data and create insightful dashboards and reports for our clients.', 'SQL, Excel, Power BI, Python', 3, '2025-07-28 04:03:23'),
(12, 'InnovaSoft Solutions', 'HR Manager', 'Human Resources', 'Full-Time', '5+ years', '₦600,000', 'Ibadan, Nigeria', 'Manage recruitment, employee engagement, and HR policy compliance at InnovaSoft.', 'Recruitment, Communication, Conflict Resolution', 3, '2025-07-28 04:03:23');

-- --------------------------------------------------------

--
-- Table structure for table `saved_jobs`
--

CREATE TABLE `saved_jobs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `job_id` int(11) NOT NULL,
  `saved_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `saved_jobs`
--

INSERT INTO `saved_jobs` (`id`, `user_id`, `job_id`, `saved_at`) VALUES
(5, 1, 7, '2025-07-28 03:42:34'),
(6, 1, 4, '2025-07-28 03:42:36'),
(7, 1, 1, '2025-07-28 03:42:42');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('job_seeker') DEFAULT 'job_seeker',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `phone` varchar(20) DEFAULT NULL,
  `preference` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `role`, `created_at`, `phone`, `preference`, `location`, `profile_picture`) VALUES
(1, 'Akinlawon', 'akin@gmail.com', 'pass', 'job_seeker', '2025-07-25 03:00:54', NULL, NULL, NULL, NULL),
(2, 'Akinlawon Michael', 'akinlawon@gmail.com', 'pass', 'job_seeker', '2025-08-05 09:03:59', NULL, NULL, NULL, NULL),
(3, 'Aina Joshua', 'aina@gmail.com', 'pass', 'job_seeker', '2025-08-19 12:40:23', '09099009900', 'Full-Time', 'Nigeria', 'imp.jpg'),
(4, 'Mich', 'mic@gmail.com', '    ', 'job_seeker', '2025-08-26 00:22:03', '08039659466', NULL, 'Lagos', NULL),
(5, 'Jamiu', 'jamiu@gmail.com', '    ', 'job_seeker', '2025-08-28 16:42:20', '09080849863', 'Full-Time', 'Ilaro', NULL),
(6, 'Bamidele Kowiyat', 'hinishegzzy7@gmail.com', '    ', 'job_seeker', '2025-08-29 02:29:24', NULL, NULL, NULL, NULL),
(7, 'Akinlawon Muaz', 'writerwritesforme@gmail.com', '    ', 'job_seeker', '2025-09-01 16:04:59', NULL, NULL, NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `employers`
--
ALTER TABLE `employers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `interviews`
--
ALTER TABLE `interviews`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `employer_id` (`employer_id`);

--
-- Indexes for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `employers`
--
ALTER TABLE `employers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `interviews`
--
ALTER TABLE `interviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`);

--
-- Constraints for table `jobs`
--
ALTER TABLE `jobs`
  ADD CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`id`);

--
-- Constraints for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  ADD CONSTRAINT `saved_jobs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `saved_jobs_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
