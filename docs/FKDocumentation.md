# Final Kid Films 3.0 Documentation
##### Last updated: 29-01-18

### Introduction
This document collects the complete workflow of Final Kid so it is clear for everyone what the best practise is and how projects should work.
### Company structure 2018
​										Charly (Founder, Director)

Employed Camera-operators/Editors	-	Final Kids (Freelancers)	-	Project Manager

​										Camera/Edit intern		-	Library Intern

# Working for Final Kid Films

### How to showcase the work you did for Final Kid Films?

### How to tag Final Kid on Social Media?

### How to include Final Kid work in your portfolio?

### What is the insurance policy and who is responsible for damage/theft of equipment?

#### How do I send an invoice to Final Kid?

#### What is reimbursed on a production?

####How do I get reimbursed for costs I made?

# Pre-Production

#### Writing a treatment

### Preparing gear for a shoot, what to bring and how

### Create a gearlist and how to submit it

# Production

## Travel

### In Europe

### Outside Europe

### Transport on location

#### Visum

#### When bringing your own gear

#### Festival Credentials

### Emergencies


## Operating a RED Camera

### Setting-up a RED camera for a shoot

#### Driveletter

#### Pre-record

#### Proxies

#### Colorspace and LUT

#### (Secure) Card Formatting

#### Image settings, resolution and framesize

#### Best practices

#### Offloading Footage


### Best practices for filming a festival
#### Best practices for filming scenics

## Datahandling


# Post-Production
## How to process footage from a shoot at the office
### Folder Naming conventions
### Project Naming Conventions
### Folder lay-out
### How to create proxies?
Proxies make editing a lot easier however there are many "gotcha's" and issues which can make working with and creating proxies difficult and frustrating. There are many ways to transcode 20 files of the same codec. However it gets more difficult to do this for 3000+ files with 3 different codecs, frame sizes and aspect ratio's. While not having to start batches and manually watch the que because this can take a long time.

Every project should have proxies because codecs such as H.264 (MP4) and Sony MXF strain the CPU heavily and are not optimized for editing. RED R3D files can have massive resolution and take a long time to load when opening a project. To keep the project running and opening smoothly as a project advances, proxy files need to be created. This will also make the project more portable as you can edit the project with only the proxy files on a small drive.

Below should be the smoothest proxy creation workflow.

1. **In-Camera:** RED Camera's from DSCM2 upwards can make proxies in camera and should do this on the shoot (See Pre-Production for explaination). So most of the RED footage should have proxies created at the shoot. You can also use an external recorder such as an Atomos Shogun.

2. **R3D footage**: should be converted with the "Final Kid RED Proxy tool" available on the Final Kid Dropbox with instructions in the folder. Other programs, such as Media Encoder lack performance and functionality to do a stable batch convert of 100+ R3D files while maintaining the right aspect ratio.

3. **"Normal codecs" such as H264 (mp4/mov), XMF:** Use Davinci Resolve 14 (Free to download),

   1. Open Davinci Resolve
   2. Create a new empty project
   3. Import all the files into Davinci you want to transcode while in the "Media" tab. You can do this by using the media browser in the "Media" tab and dragging all the files in the project bin area .
   4. Go to the "Edit" tab
   5. Drag all the files onto the timeline.
   6. Go to the "Deliver" tab.
   7. In the upper left you should see the "Render settings" tab
   8. Select Browse to set the output location to the "09_Proxies" folder of your project.
   9. Select Render: Individual clips
   10. Video tab: Format Quicktime, Codec ProRess 422 LT, Resolution: 1920 x 1080
   11. Go to the audio tab, Codec: Linear PCM, **Channels: Same as source**, Bit Depth: 16
   12. Go to the File tab, Filename uses: Source name
   13. Press the "Add to Render que" button
   14. The render job should now appear on the right side of the screen
   15. Start the render with the "Start Render" button in the "Render Que" tab
   16. Grab a coffee while waiting.

   (Premiere's Pro Ingest, Media Encoder, iffmpeg, Handbrake, Squarebox, and a lot of other conversion tools lack stability or functionality to do a proper batch convert, I tried them all haha.)

**Codec Format**

The proxy format we found with the best quality, file size and availibility is ProRess 422 LT. Therefor this is the standard Proxy format we use.

Proxy Format: ProRess 422 LT

Container: MOV

Size: Height 1920 Width: 1080  (Width is dependant on the Aspect ratio of the source footage, 21:9 becomes approximately 1920 x 810 for example). 1080p is chosen over 720p because with 1080p you can render intermediate versions for clients from the proxies without too much quality loss without having to render from the source files.

Frame Rate: Same as source

**Output**

Output Folder: "09_Proxies" in your project folder. All proxies end up in the same folder. Make sure there are no duplicate file(names). So you are left with 1 folder with all the proxy clips for the project.

Output file names: Same as source (otherwise Premiere Pro can't auto relink the files)

### How to plan an edit?

## Setting up a Premiere Pro Project

### Setting up a project

#### Importing footage

Attaching Proxies

#### Creating Timelines
Offlining Source files

#### Spotting footage

1. Create a new sequence with the right settings for the project and name it "SCENICS_DUMP", create another for "FESTIVAL_DUMP". As the names suggest, the Scenics timeline will hold all the raw scenerary footage and the Festival_dump will hold all the the RAW footage related to the festival itself.
2. On these timelines you put all the footage of the project. The timeline holds all the video files being used in the project.
3. Duplicate the timelines and call them "FESTIVAL_SELECTION" and "SCENICS_SELECTION", these are the timelines in which you will do the actual spotting.

#### Categorizing Spotted Footage

**Working with versions in your timeline **

#### How to export a video?

##### Intermediate export (V0, V1, V2)

##### Final export

#### Video is done, how to archive the project?

## Editing a video, best practices

#### Shortkeys

#### Create flow

#### Color Grading

#### Sound Design

## How and when to deliver video versions and ask for feedback?

### How to transfer large files over the internet?
