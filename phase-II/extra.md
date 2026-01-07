
BETTER_AUTH_SECRET: (Your generated secret)
Deploy. Copy the URL (e.g., https://my-backend.vercel.app).
Step 2: Deploy the Frontend
Create a New Project in Vercel.
Import the same repository.
Set Root Directory to 
frontend
.
Add these Environment Variables:
DATABASE_URL: postgresql://neondb_owner:npg_ay7VmDYWv5pF@ep-super-leaf-a187t6fa-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET: LKA0MD6mwFSKmix2G7VrKmfYH8l8iO_Jsxo0T5bsLZM
NEXT_PUBLIC_API_URL: https://hackahton-ii-phase-r7kdvv6ps-laibas-projects-9db21535.vercel.app
BETTER_AUTH_URL: (Aapka frontend URL, e.g., https://hackathon-ii-frontend.vercel.app)
Deploy