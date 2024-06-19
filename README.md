# Work Portal System

A system offers solutions for **HR**, **IT**, **Project** management. It is aimed to make workflow more smooth, paperless, and efficient.

As a `HR manager`, you can manager department, employee, schedule, timeoff, etc.

As a `IT technician`, you can manager the IT Ticket, IT Asset, etc.

As a `Project manager`, you can manager the Project process, Task of Project, etc.

## Features

- 🧩**All The Building Blocks You Need**: Provides useful functionalities, such as `Employee management`, `Clocking system`, `Leaving management`, `IT asset management`, `IT ticket management`, `Project management`, and etc.
- 🤟**High Quality**: Widely-accessible, responsive, secure, and fast.
- 🆓**Ulimit & Free**: No user account limit, No monthly fee.
- 💯**Powered by**: Cerek Shi, a solo full stack developer.

# Work Portal Server Architecture

![WorkPortal-Server-Architecture](https://wiki.wildsre.com/github/workportal_architecture.png)

**Work Portal Server** comes with an all-in-one software architecture.

**Work Portal Server** was built by [Django REST Framewrok](https://www.django-rest-framework.org/) as backend server, which offers the API Service for various clients. All the data will be saved to [MySQL Database](https://www.mysql.com/) in production environment. We also use the [Redis Server](https://redis.io/) as caching server to improve performance.

**Work Portal Server** offers various clients for different scenarios.

- **Web Client Support**: It's a front-end application built with [Work Portal Web](https://github.com/cerek/work-portal-web), and the interface will be used for all login users.
- **Phone App Support**: We will offer the mobile solution in the future.
- **Terminal Support**: [`IT technician only`] It's a command line tool to create/update data quickly.
- **FingerPrint Machine**: Integrate with a self-built fingerprint machine to record the punch-in/out in clocking system.

## Documentation

- **User Guide**: -
- **API Docs**: -

## Related Repo

- **Back-end Server**: [Work Portal Server](https://github.com/cerek/work-portal-server/)
- **Web Client**: [Work Portal Web](https://github.com/cerek/work-portal)
- **Phone App Client**:
  - [iOS]()
  - [Android]()
- **Terminal Client**: -
- **FingerPrint Machine**: -
