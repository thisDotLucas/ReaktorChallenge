# ReaktorChallenge
Live version -> https://thisdotlucas.pythonanywhere.com

## Goal
The goal is to display key information about a /var/lib/dpkg/status file that holds information about software packages that the system knows about in Ubuntu and Debian systems.
All data should be displayed in a Html interface, with the index page having the packages sorted in alphabetical order. All packages and dependencies should be displayed as links
that link to the corresponding package with its key information.

### Key information
<ul>
  <li>Package name</li>
  <li>Dependencies</li>
  <li>Reverse dependencies</li>
  <li>Description</li>
</ul>

## Approach
I mapped the relevant information into dictonaries and
I used Python Flask as it is easy to just create one single template for every package to display the data. I used the request and bs4 package to get the mock data as text.

