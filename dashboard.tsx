  <Link href={item.link} key={item.id} className="w-[280px]">
            <Card className="shadow-md transition-transform hover:scale-105 cursor-pointer">
              <CardHeader>
                <CardTitle>{item.name}</CardTitle>
                <CardDescription>{item.description}</CardDescription>
              </CardHeader>
            </Card>
          </Link>