# Food Surplus Platform DevOps Laboratory

Personal DevOps laboratory project for **Danil Kukurekin**, group **IT2-2312**, Student ID **37554**. The Python application models a small food-surplus marketplace: a business lists an offer and a recipient reserves only the quantity still available.

## Project structure

```text
kukurekin_danil/
├── app/                         # FastAPI MVP
├── scripts/                     # Bash scripts for the Linux demonstration
├── config/app.conf              # Application configuration example
├── logs/application.log         # Generated locally and ignored by Git
├── backup/                      # Local backup directory, ignored by Git
├── tests/                       # API tests, including overselling protection
├── Dockerfile
├── docker-compose.yml
└── Jenkinsfile
```

## Linux demonstration

```bash
cd ~/devops/kukurekin_danil
pwd
ls -la
chmod +x scripts/*.sh
./scripts/Kukurekin_Danil_system.sh
./scripts/create_demo_log.sh
find . -name application.log
grep ERROR logs/application.log
grep WARNING logs/application.log
grep -c ERROR logs/application.log
tail -n 5 logs/application.log

touch private.txt public.txt
chmod 600 private.txt
chmod 644 public.txt
ls -l private.txt public.txt
ps aux | head -n 5
top
```

Use `cp`, `mv` and `rm` safely with copies during the demonstration, for example: `cp Kukurekin_Danil_info.txt backup/info-copy.txt`, `mv backup/info-copy.txt backup/student-info.txt`, then `rm backup/student-info.txt`.

Permissions: `r` means read, `w` write, `x` execute. `600` makes `private.txt` readable/writable only by its owner. `644` lets other users read `public.txt`, while only its owner can modify it.

## Local application and test

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
./scripts/run_checks.sh
uvicorn app.main:app --reload
```

Open `http://localhost:8010/docs` after a Docker run, or `http://localhost:8000/docs` when running Uvicorn directly. `GET /` displays the required student information; `POST /offers/{offer_id}/reserve` returns `409 Conflict` when a request would exceed the available quantity.

## Git workflow

The required remote repository name is **kukurekin-danil-devops**. Before the first commit, verify the identity:

```bash
git config --local user.name "D0KKKA"
git config --local user.email "danil.kukurekin@bk.ru"
git config --local --get user.email
```

After signing in to the personal GitHub account with a verified `danil.kukurekin@bk.ru` email, publish safely with:

```bash
chmod +x scripts/publish_to_github.sh
./scripts/publish_to_github.sh
```

The script checks the GitHub account's verified email before it creates a public repository, adds `origin`, or pushes commits. It deliberately stops on an account mismatch.

Demonstrate `.gitignore` after generating the log:

```bash
git status --ignored
git check-ignore -v logs/application.log backup/demo.txt .env
```

Create and merge the required branch:

```bash
git switch -c development
echo "Development branch update" >> config/app.conf
git add config/app.conf && git commit -m "Update application configuration"
git switch main
git merge development
git log --oneline --graph --all
```

## Docker demonstration

```bash
docker build -t kukurekin-danil-devops .
docker run --name kukurekin-danil-container -p 8010:8000 \
  -e STUDENT_NAME=Danil \
  -e STUDENT_SURNAME=Kukurekin \
  -e STUDENT_GROUP=IT2-2312 \
  -e STUDENT_ID=37554 \
  kukurekin-danil-devops
docker ps -a
docker logs kukurekin-danil-container
docker stop kukurekin-danil-container
docker start kukurekin-danil-container
docker rm -f kukurekin-danil-container

docker compose up --build -d
docker compose ps
docker compose logs
docker compose down
```

A Docker image is a reusable, immutable application template. A container is a running instance of that image. Environment variables keep deploy-time values outside the image; secrets must never be hard-coded into an image or committed to Git.

## Jenkins

Create a Pipeline job named **Kukurekin_Danil_DevOps** and set its Pipeline Definition to **Pipeline script from SCM**. Use the `main` branch of the GitHub repository. The committed `Jenkinsfile` performs Checkout, Build, Test, Docker Build and Docker Run. Jenkins must be configured on a machine whose agent can execute Docker commands.

## Submission checklist

- Public/access-granted GitHub repository: `https://github.com/<your-personal-account>/kukurekin-danil-devops`
- PDF report prepared separately with screenshots taken from your actual computer
- One continuous 10-20 minute video: screen + your voice, starting with your name, group and Student ID
- Jenkins console showing `Finished: SUCCESS`, the commit hash, image and running container
